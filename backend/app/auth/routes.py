from flask import request, jsonify
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    create_refresh_token,
    get_jwt
)

from .. import db, auth_bp
from ..models import User


@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    # Validate request body
    if not data:
        return jsonify({'message': 'No input data provided'}), 400

    # Required fields
    required_fields = ['username', 'password', 'name', 'email']

    # Validate empty/missing fields
    for field in required_fields:
        if not data.get(field):
            return jsonify({'message': f'{field} is required'}), 400

    # Basic email validation
    if '@' not in data['email']:
        return jsonify({'message': 'Invalid email address'}), 400

    # Check if username already exists
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'message': 'Username already exists'}), 400

    # Check if email already exists
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'message': 'Email already exists'}), 400

    # Create new user
    user = User(
        username=data['username'],
        password=data['password'],
        name=data['name'],
        email=data['email'],
        photo=data.get('photo')
    )

    db.session.add(user)
    db.session.commit()

    return jsonify({
        'message': 'User registered successfully',
        'user': {
            'id': user.id,
            'username': user.username,
            'name': user.name,
            'email': user.email
        }
    }), 201


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    # Validate request body
    if not data:
        return jsonify({'message': 'No input data provided'}), 400

    # Validate required fields
    required_fields = ['username', 'password']

    for field in required_fields:
        if not data.get(field):
            return jsonify({'message': f'{field} is required'}), 400

    username = data['username']
    password = data['password']

    # Find user
    user = User.query.filter_by(username=username).first()

    # Validate credentials
    if not user or not user.check_password(password):
        return jsonify({
            'message': 'Invalid username or password'
        }), 401

    # Create JWT tokens
    access_token = create_access_token(identity=str(user.id))
    refresh_token = create_refresh_token(identity=str(user.id))

    return jsonify({
        'message': 'Login successful',
        'access_token': access_token,
        'refresh_token': refresh_token,
        'user': {
            'id': user.id,
            'username': user.username,
            'name': user.name,
            'email': user.email,
            'photo': user.photo
        }
    }), 200


@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():

    # Token identifier (optional blacklist usage later)
    jti = get_jwt()["jti"]

    return jsonify({
        'message': 'Logout successful'
    }), 200