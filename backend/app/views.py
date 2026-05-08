from . import app, db
from flask import request, jsonify, send_file, send_from_directory
from sqlalchemy import func
import os
from .models import *
from werkzeug.utils import secure_filename
from flask_jwt_extended import (
    create_access_token, create_refresh_token,
    jwt_required, get_jwt_identity, get_jwt
)
from werkzeug.security import check_password_hash
import cloudinary.uploader


revoked_tokens = set()

@app.route('/api/uploads/<filename>')
def get_uploaded_file(filename):
    return send_from_directory(os.path.join(os.getcwd(), app.config['UPLOAD_FOLDER']), filename)

@app.route('/api/register', methods=['POST'])
def register():

    try:

        # CHECK CONTENT TYPE
        if not request.content_type.startswith(
            'multipart/form-data'
        ):
            return jsonify(
                error="Unsupported content type"
            ), 415

        # FORM DATA
        username = request.form.get('username')
        password = request.form.get('password')
        name = request.form.get('name')
        email = request.form.get('email')

        # FILE
        photo = request.files.get('photo')

        # REQUIRED FIELDS
        if not all([
            username,
            password,
            name,
            email
        ]):
            return jsonify(
                error="Missing required fields"
            ), 400

        # DUPLICATE USERNAME
        if User.query.filter_by(
            username=username
        ).first():

            return jsonify(
                error="Username already exists"
            ), 409

        # DUPLICATE EMAIL
        if User.query.filter_by(
            email=email
        ).first():

            return jsonify(
                error="Email already exists"
            ), 409

        # DEFAULT PHOTO URL
        photo_url = None

        # =========================
        # CLOUDINARY IMAGE UPLOAD
        # =========================

        if photo and photo.filename != '':

            allowed_extensions = {
                'png',
                'jpg',
                'jpeg',
                'gif',
                'webp'
            }

            filename = secure_filename(
                photo.filename
            )

            # CHECK EXTENSION
            if '.' not in filename:

                return jsonify(
                    error="Invalid file"
                ), 400

            ext = filename.rsplit(
                '.',
                1
            )[-1].lower()

            if ext not in allowed_extensions:

                return jsonify(
                    error="Invalid image extension"
                ), 400

            try:

                upload_result = cloudinary.uploader.upload(
                    photo,
                    folder="jamdate_profiles"
                )

                photo_url = upload_result.get(
                    "secure_url"
                )

            except Exception as cloudinary_error:

                print(
                    "CLOUDINARY ERROR:",
                    str(cloudinary_error)
                )

                return jsonify({
                    "error":
                    "Cloudinary upload failed",

                    "details":
                    str(cloudinary_error)
                }), 500

        # =========================
        # CREATE USER
        # =========================

        new_user = User(
            username=username,
            password=password,
            name=name,
            email=email,
            photo=photo_url
        )

        db.session.add(new_user)

        db.session.commit()

        # SUCCESS
        return jsonify({

            "message":
            "User created successfully",

            "user":
            new_user.to_dict()

        }), 201

    except Exception as e:

        print("REGISTER ERROR:", str(e))

        return jsonify({

            "error":
            "Registration failed",

            "details":
            str(e)

        }), 500

@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.get_json()

    user = User.query.filter_by(username=data.get('username')).first()
    
    if not user or not check_password_hash(user.password, data.get('password')):
        return jsonify({"error": "Invalid credentials"}), 401

    access_token = create_access_token(identity=str(user.id))
    refresh_token = create_refresh_token(identity=str(user.id))
    
    return jsonify(message="Login successful",
                   access_token=access_token,
                   refresh_token=refresh_token,
                   user=user.to_dict()
            ), 200

@app.route('/api/auth/logout', methods=['POST'])
@jwt_required()
def logout():
    jti = get_jwt()["jti"]
    revoked_tokens.add(jti)
    return jsonify(message="Successfully logged out"), 200

@app.route('/api/profiles', methods=['GET', 'POST'])
@jwt_required()
def profiles():

    current_user = get_jwt_identity()
    user_id = int(current_user)

    if request.method == 'GET':

        blocked_users = db.session.query(
            BlockedUser.blocked_id
        ).filter(
            BlockedUser.blocker_id == user_id
        )

        blocked_by_users = db.session.query(
            BlockedUser.blocker_id
        ).filter(
            BlockedUser.blocked_id == user_id
        )

        passed_users = db.session.query(
            Pass.passed_user_id_fk
        ).filter(
            Pass.user_id_fk == user_id
        )

        profiles = Profile.query.filter(
            Profile.is_public == True,
            Profile.user_id_fk != user_id,
            ~Profile.user_id_fk.in_(blocked_users),
            ~Profile.user_id_fk.in_(blocked_by_users),
            ~Profile.user_id_fk.in_(passed_users)
        ).all()

        profile_list = [
            profile.to_dict() for profile in profiles
        ]

        return jsonify(profiles=profile_list), 200

    else:

        data = request.get_json()

        # Interests list from frontend
        interests_data = data.get('interests', [])

        required = [
            'description',
            'parish',
            'biography',
            'sex',
            'race',
            'birth_year',
            'height',
            'fav_cuisine',
            'fav_colour',
            'fav_school_subject',
            'political',
            'religious',
            'family_oriented'
        ]

        if not all(field in data for field in required):
            return jsonify({
                "error": "Missing required fields"
            }), 400

        # Prevent duplicate profiles
        existing_profile = Profile.query.filter_by(
            user_id_fk=user_id
        ).first()

        if existing_profile:
            return jsonify({
                "error": "User already has a profile"
            }), 400

        new_profile = Profile(
            user_id_fk=user_id,
            description=data['description'],
            parish=data['parish'],
            biography=data['biography'],
            sex=data['sex'],
            race=data['race'],
            birth_year=data['birth_year'],
            height=data['height'],
            fav_cuisine=data['fav_cuisine'],
            fav_colour=data['fav_colour'],
            fav_school_subject=data['fav_school_subject'],
            political=data['political'],
            religious=data['religious'],
            family_oriented=data['family_oriented'],

            # OPTIONAL FEATURE — Public/Private Profiles
            is_public=data.get('is_public', True)
        )

        # Add interests to profile
        for interest_name in interests_data:

            # Skip empty values
            if not interest_name.strip():
                continue

            # Check if interest already exists
            interest = Interest.query.filter_by(
                name=interest_name.strip()
            ).first()

            # Create new interest if it doesn't exist
            if not interest:

                interest = Interest(
                    name=interest_name.strip()
                )

                db.session.add(interest)

            # Link interest to profile
            new_profile.interests.append(interest)

        db.session.add(new_profile)
        db.session.commit()

        return jsonify(
            message="Profile created successfully",
            profile=new_profile.to_dict()
        ), 201

@app.route('/api/profiles/mutual-matches', methods=['GET'])
@jwt_required()
def get_mutual_matches():
    current_user_id = int(get_jwt_identity())

    # Alias so we can self-join favourites
    f1 = db.aliased(Favourite)
    f2 = db.aliased(Favourite)

    # f1 = rows where I liked someone
    # f2 = rows where that someone liked me back
    mutual_user_ids = db.session.query(f1.fav_user_id_fk).join(
        f2,
        db.and_(
            f1.fav_user_id_fk == f2.user_id_fk,   # The person I liked also liked...
            f2.fav_user_id_fk == f1.user_id_fk    # ...me back
        )
    ).filter(
        f1.user_id_fk == current_user_id           # I am the one who liked first
    )

    mutual_profiles = Profile.query.filter(
        Profile.user_id_fk.in_(mutual_user_ids),
        Profile.is_public == True
    ).all()

    return jsonify(profiles=[p.to_dict() for p in mutual_profiles]), 200


@app.route('/api/profiles/<int:profile_id>', methods=['GET'])
@jwt_required()
def get_profile(profile_id):
    profile = Profile.query.filter_by(id=profile_id).first()

    if not profile:
        return jsonify(error="Profile not found"), 404

    return jsonify(profile=profile.to_dict()), 200


@app.route('/api/profiles/<int:profile_id>', methods=['PUT'])
@jwt_required()
def update_profile(profile_id):
    current_user_id = int(get_jwt_identity())
    profile = Profile.query.filter_by(id=profile_id, user_id_fk=current_user_id).first()

    if not profile:
        return jsonify({"error": "Profile not found or unauthorized"}), 404

    data = request.get_json()

    for field in ['description', 'parish', 'biography', 'sex', 'race', 'birth_year',
                  'height', 'fav_cuisine', 'fav_colour', 'fav_school_subject',
                  'political', 'religious', 'family_oriented', 'is_public']:
        if field in data:
            setattr(profile, field, data[field])

    if 'interests' in data:
        profile.interests.clear()
        for interest_name in data['interests']:
            if not interest_name.strip():
                continue
            interest = Interest.query.filter_by(name=interest_name.strip()).first()
            if not interest:
                interest = Interest(name=interest_name.strip())
                db.session.add(interest)
            profile.interests.append(interest)

    db.session.commit()
    return jsonify(message="Profile updated successfully", profile=profile.to_dict()), 200


@app.route('/api/profiles/<int:user_id>/favourite', methods=['POST'])
@jwt_required()
def favourite(user_id):
    current_user_id = int(get_jwt_identity())
    fav_user_id = user_id

    if current_user_id == fav_user_id:
        return jsonify({"error": "Cannot Favourite Yourself"}), 400

    existing_fav = Favourite.query.filter_by(
        user_id_fk=current_user_id,
        fav_user_id_fk=fav_user_id
    ).first()

    if existing_fav:
        return jsonify({"error": "User Already in Favourites"}), 400

    fav_user = User.query.get(fav_user_id)
    if not fav_user:
        return jsonify({"error": "User not found"}), 404

    new_fav = Favourite(
        user_id_fk=current_user_id,
        fav_user_id_fk=fav_user_id
    )

    db.session.add(new_fav)
    db.session.commit()

    return jsonify({"message": "User added to Favorites"}), 201


@app.route('/api/profiles/<int:user_id>/favourite', methods=['DELETE'])
@jwt_required()
def remove_favourite(user_id):
    current_user_id = int(get_jwt_identity())

    existing_fav = Favourite.query.filter_by(
        user_id_fk=current_user_id,
        fav_user_id_fk=user_id
    ).first()

    if not existing_fav:
        return jsonify({"error": "Not in favourites"}), 404

    db.session.delete(existing_fav)
    db.session.commit()

    return jsonify({"message": "Removed from favourites"}), 200


@app.route('/api/profiles/<int:user_id>/pass', methods=['POST'])
@jwt_required()
def pass_profile(user_id):
    current_user_id = int(get_jwt_identity())

    if current_user_id == user_id:
        return jsonify({"error": "Cannot pass yourself"}), 400

    existing = Pass.query.filter_by(
        user_id_fk=current_user_id,
        passed_user_id_fk=user_id
    ).first()

    if existing:
        return jsonify({"message": "Already passed"}), 200

    db.session.add(Pass(user_id_fk=current_user_id, passed_user_id_fk=user_id))
    db.session.commit()
    return jsonify({"message": "Profile passed"}), 201


@app.route('/api/profiles/matches/<int:profile_id>', methods=['GET'])
@jwt_required()
def get_profile_matches(profile_id):

    base_profile = Profile.query.get(profile_id)

    if not base_profile:
        return jsonify(error="Profiles not found"), 404

    candidates = Profile.query.filter(
        Profile.id != base_profile.id,
        Profile.user_id_fk != base_profile.user_id_fk,
        Profile.is_public == True,
    ).all()

    # OPTIONAL FEATURE — Hide blocked users
    blocked_users = db.session.query(
        BlockedUser.blocked_id
    ).filter(
        BlockedUser.blocker_id == base_profile.user_id_fk
    )

    blocked_by_users = db.session.query(
        BlockedUser.blocker_id
    ).filter(
        BlockedUser.blocked_id == base_profile.user_id_fk
    )

    matched_profiles = []

    for profile in candidates:

        if profile.user_id_fk in blocked_users:
            continue

        if profile.user_id_fk in blocked_by_users:
            continue

        match_count = 0

        if profile.fav_cuisine and base_profile.fav_cuisine and profile.fav_cuisine == base_profile.fav_cuisine:
            match_count += 1

        if profile.fav_colour and base_profile.fav_colour and profile.fav_colour == base_profile.fav_colour:
            match_count += 1

        if profile.fav_school_subject and base_profile.fav_school_subject and profile.fav_school_subject == base_profile.fav_school_subject:
            match_count += 1

        if profile.political == base_profile.political:
            match_count += 1

        if profile.religious == base_profile.religious:
            match_count += 1

        if profile.family_oriented == base_profile.family_oriented:
            match_count += 1

        # Age within 10 years is a bonus point
        if base_profile.birth_year and profile.birth_year:
            if abs(profile.birth_year - base_profile.birth_year) <= 10:
                match_count += 1

        # Height within 20 cm is a bonus point
        if base_profile.height and profile.height:
            if abs(profile.height - base_profile.height) <= 20:
                match_count += 1

        shared_interests = set(
            interest.name for interest in profile.interests
        ).intersection(
            set(interest.name for interest in base_profile.interests)
        )
        match_count += len(shared_interests)

        if match_count >= 3:
            profile_data = profile.to_dict()
            profile_data['compatibility'] = round((match_count / 8) * 100)
            matched_profiles.append(profile_data)

    return jsonify(profiles=matched_profiles), 200

@app.route('/api/search', methods=['GET'])
@jwt_required()
def search():
    current_user = get_jwt_identity()
    user_id = int(current_user)

    name          = request.args.get('name')
    birth_year    = request.args.get('birth_year', type=int)
    sex           = request.args.get('sex')
    race          = request.args.get('race')
    parish        = request.args.get('parish')
    interests     = request.args.get('interests')
    gender        = request.args.get('gender')
    date_of_birth = request.args.get('date_of_birth')

    query = db.session.query(Profile).join(User)

    # Do not show current user
    query = query.filter(Profile.user_id_fk != user_id)

    # OPTIONAL FEATURE — Only show public profiles
    query = query.filter(Profile.is_public == True)

    if name:
        query = query.filter(func.lower(User.name).like(f"%{name.lower()}%"))

    if birth_year:
        query = query.filter(Profile.birth_year == birth_year)

    if sex:
        query = query.filter(func.lower(Profile.sex).like(f'%{sex.lower()}%'))

    if race:
        query = query.filter(func.lower(Profile.race).like(f'%{race.lower()}%'))

    # gender is applied only when sex is not already provided
    if gender and not sex:
        query = query.filter(func.lower(Profile.sex).like(f'%{gender.lower()}%'))

    # date_of_birth is applied only when birth_year is not already provided
    if date_of_birth and not birth_year:
        try:
            # Supports both "1995" and "1995-06-20"
            dob_year = int(date_of_birth.split('-')[0])
            query = query.filter(Profile.birth_year == dob_year)
        except (ValueError, AttributeError):
            return jsonify({"error": "Invalid date_of_birth format. Use YYYY or YYYY-MM-DD"}), 400

    if parish:
        query = query.filter(func.lower(Profile.parish).like(f'%{parish.lower()}%'))

    if interests:
        interest_list = [i.strip().lower() for i in interests.split(',') if i.strip()]
        if interest_list:
            query = query.join(Profile.interests).filter(
                func.lower(Interest.name).in_(interest_list)
            ).distinct()

    # OPTIONAL FEATURE — Hide blocked users
    blocked_users = db.session.query(BlockedUser.blocked_id).filter(
        BlockedUser.blocker_id == user_id
    )

    blocked_by_users = db.session.query(BlockedUser.blocker_id).filter(
        BlockedUser.blocked_id == user_id
    )

    query = query.filter(
        ~Profile.user_id_fk.in_(blocked_users),
        ~Profile.user_id_fk.in_(blocked_by_users)
    )

    results = query.all()

    profiles = [profile.to_dict() for profile in results]

    return jsonify(profiles=profiles), 200


@app.route('/api/users/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user(user_id):
    user = User.query.filter_by(id=user_id).first()

    if not user:
        return jsonify(error="User not found"), 404

    return jsonify(user=user.to_dict()), 200


@app.route('/api/users/<int:user_id>/profile', methods=['GET'])
@jwt_required()
def get_user_profile(user_id):
    profile = Profile.query.filter_by(user_id_fk=user_id).first()

    if not profile:
        return jsonify({"error": "Profile not found"}), 404

    return jsonify(profile=profile.to_dict()), 200

@app.route('/api/users/<user_id>/favourites', methods=['GET'])
@jwt_required()
def get_favourite_users(user_id):
    sort_by = request.args.get('sort_by', 'name')
    order   = request.args.get('order', 'asc')

    valid_sorts = ['name', 'parish', 'age']
    if sort_by not in valid_sorts:
        return jsonify({"error": "Invalid sort parameter"}), 400

    query = db.session.query(User).join(
        Favourite, User.id == Favourite.fav_user_id_fk).filter(
        Favourite.user_id_fk == user_id
    )

    if sort_by == 'name':
        query = query.order_by(User.name.asc() if order == 'asc' else User.name.desc())
    elif sort_by == 'parish':
        query = query.join(Profile).order_by(
            Profile.parish.asc() if order == 'asc' else Profile.parish.desc()
        )
    elif sort_by == 'age':
        current_year = datetime.now().year
        query = query.join(Profile).order_by(
            (current_year - Profile.birth_year).asc() if order == 'asc' else (current_year - Profile.birth_year).desc()
        )

    favourites = query.all()
    return jsonify([user.to_dict() for user in favourites]), 200

@app.route('/api/block/<int:user_id>', methods=['POST'])
@jwt_required()
def block_user(user_id):

    blocker_id = int(get_jwt_identity())

    if blocker_id == user_id:
        return jsonify({
            "error": "Cannot block yourself"
        }), 400

    user_to_block = User.query.get(user_id)

    if not user_to_block:
        return jsonify({
            "error": "User not found"
        }), 404

    existing_block = BlockedUser.query.filter_by(
        blocker_id=blocker_id,
        blocked_id=user_id
    ).first()

    if existing_block:
        return jsonify({
            "error": "User already blocked"
        }), 400

    blocked_user = BlockedUser(
        blocker_id=blocker_id,
        blocked_id=user_id
    )

    db.session.add(blocked_user)
    db.session.commit()

    return jsonify({
        "message": "User blocked successfully"
    }), 201

@app.route('/api/users/favourites/<N>', methods=['GET'])
@jwt_required()
def get_top_favourites(N):
    try:
        N = int(N)
        if N <= 0:
            raise ValueError
    except ValueError:
        return jsonify({"error": "N must be a Positive Integer"}), 400

    sort_by = request.args.get('sort_by', 'count')
    order   = request.args.get('order', 'desc')

    query = db.session.query(
        User,
        db.func.count(Favourite.id).label('favourite_count')
    ).join(
        Favourite, User.id == Favourite.fav_user_id_fk
    ).group_by(User.id)

    if sort_by == 'count':
        query = query.order_by(
            db.desc('favourite_count') if order == 'desc' else db.asc('favourite_count')
        )
    elif sort_by == 'name':
        query = query.order_by(
            User.name.asc() if order == 'asc' else User.name.desc()
        )
    elif sort_by == 'parish':
        query = query.join(Profile).order_by(
            Profile.parish.asc() if order == 'asc' else Profile.parish.desc()
        )
    elif sort_by == 'age':
        current_year = datetime.now().year
        query = query.join(Profile).order_by(
            (current_year - Profile.birth_year).asc() if order == 'asc' else (current_year - Profile.birth_year).desc()
        )

    top_users = query.limit(N).all()

    result = []
    for user, count in top_users:
        user_data = user.to_dict()
        user_data['favourite_count'] = count
        result.append(user_data)

    return jsonify(result), 200
@app.route('/api/messages/conversations', methods=['GET'])
@jwt_required()
def get_conversations():
    current_user_id = int(get_jwt_identity())

    sent_to = db.session.query(Message.receiver_id).filter(
        Message.sender_id == current_user_id
    ).distinct()

    received_from = db.session.query(Message.sender_id).filter(
        Message.receiver_id == current_user_id
    ).distinct()

    partner_ids = set(
        [r[0] for r in sent_to.all()] + [r[0] for r in received_from.all()]
    )

    conversations = []
    for partner_id in partner_ids:
        partner = User.query.get(partner_id)
        if not partner:
            continue

        last_message = Message.query.filter(
            ((Message.sender_id == current_user_id) & (Message.receiver_id == partner_id)) |
            ((Message.sender_id == partner_id) & (Message.receiver_id == current_user_id))
        ).order_by(Message.timestamp.desc()).first()

        conversations.append({
            'user': partner.to_dict(),
            'last_message': last_message.to_dict() if last_message else None
        })

    conversations.sort(
        key=lambda x: x['last_message']['timestamp'] if x['last_message'] else '',
        reverse=True
    )

    return jsonify(conversations=conversations), 200


@app.route('/api/messages', methods=['POST'])
@jwt_required()
def send_message():

    sender_id = int(get_jwt_identity())

    data = request.get_json()

    receiver_id = data.get('receiver_id')
    content = data.get('content')

    if not receiver_id or not content:
        return jsonify({
            "error": "receiver_id and content are required"
        }), 400

    if sender_id == receiver_id:
        return jsonify({
            "error": "Cannot message yourself"
        }), 400

    receiver = User.query.get(receiver_id)

    if not receiver:
        return jsonify({
            "error": "Receiver not found"
        }), 404

    # OPTIONAL FEATURE — Blocked users cannot message each other
    blocked = BlockedUser.query.filter(
        (
            (BlockedUser.blocker_id == sender_id) &
            (BlockedUser.blocked_id == receiver_id)
        ) |
        (
            (BlockedUser.blocker_id == receiver_id) &
            (BlockedUser.blocked_id == sender_id)
        )
    ).first()

    if blocked:
        return jsonify({
            "error": "Messaging unavailable"
        }), 403

    new_message = Message(
        sender_id=sender_id,
        receiver_id=receiver_id,
        content=content
    )

    db.session.add(new_message)
    db.session.commit()

    return jsonify({
        "message": "Message sent successfully",
        "data": new_message.to_dict()
    }), 201

@app.route('/api/messages/<int:user_id>', methods=['GET'])
@jwt_required()
def get_conversation(user_id):

    current_user_id = int(get_jwt_identity())

    other_user = User.query.get(user_id)

    if not other_user:
        return jsonify({
            "error": "User not found"
        }), 404

    # OPTIONAL FEATURE — Blocked users cannot view conversations
    blocked = BlockedUser.query.filter(
        (
            (BlockedUser.blocker_id == current_user_id) &
            (BlockedUser.blocked_id == user_id)
        ) |
        (
            (BlockedUser.blocker_id == user_id) &
            (BlockedUser.blocked_id == current_user_id)
        )
    ).first()

    if blocked:
        return jsonify({
            "error": "Conversation unavailable"
        }), 403

    messages = Message.query.filter(
        (
            (Message.sender_id == current_user_id) &
            (Message.receiver_id == user_id)
        ) |
        (
            (Message.sender_id == user_id) &
            (Message.receiver_id == current_user_id)
        )
    ).order_by(Message.timestamp.asc()).all()

    return jsonify({
        "messages": [message.to_dict() for message in messages]
    }), 200
    
@app.route('/')
def index():
    return jsonify(message="This is the beginning of our API")


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also tell the browser not to cache the rendered page.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response