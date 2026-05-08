from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flask import url_for


profile_interests = db.Table(
    'profile_interests',
    db.Column('profile_id', db.Integer, db.ForeignKey('profiles.id')),
    db.Column('interest_id', db.Integer, db.ForeignKey('interests.id'))
)

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    photo = db.Column(db.String(200))
    date_joined = db.Column(db.DateTime, default=datetime.now)
    
    profiles = db.relationship('Profile', backref='user', lazy=True)
    favorites = db.relationship('Favourite', foreign_keys='Favourite.user_id_fk', backref='user', lazy=True)

    def __init__(self, username, password, name, email, photo=None):
        self.username = username
        self.set_password(password)
        self.name = name
        self.email = email
        self.photo = photo

    def get_id(self):
        return str(self.id)

    def __repr__(self):
        return f'<User {self.username}>'
    
    def set_password(self, password):
        self.password = generate_password_hash(password, method='pbkdf2:sha256')
    
    def check_password(self, password):
        return check_password_hash(self.password, password)

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "name": self.name,
            "email": self.email,
            "photo": self.photo if self.photo else None,
            "date_joined": self.date_joined.strftime("%Y-%m-%d %H:%M:%S") if self.date_joined else None
        }

class Interest(db.Model):
    __tablename__ = 'interests'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)

    def __repr__(self):
        return f'<Interest {self.name}>'

class Profile(db.Model):
    __tablename__ = 'profiles'
    
    id = db.Column(db.Integer, primary_key=True)

    user_id_fk = db.Column(
        db.Integer,
        db.ForeignKey('users.id'),
        nullable=False
    )

    description = db.Column(db.String(500))
    parish = db.Column(db.String(50))
    biography = db.Column(db.String(1000))
    sex = db.Column(db.String(20))
    race = db.Column(db.String(50))
    birth_year = db.Column(db.Integer)
    height = db.Column(db.Float)
    fav_cuisine = db.Column(db.String(50))
    fav_colour = db.Column(db.String(30))
    fav_school_subject = db.Column(db.String(50))
    political = db.Column(db.Boolean)
    religious = db.Column(db.Boolean)
    family_oriented = db.Column(db.Boolean)

    # OPTIONAL FEATURE — Profile Visibility
    is_public = db.Column(
        db.Boolean,
        default=True
    )

    interests = db.relationship(
        'Interest',
        secondary=profile_interests,
        backref='profiles'
    )

    def __init__(
        self,
        user_id_fk,
        description=None,
        parish=None,
        biography=None,
        sex=None,
        race=None,
        birth_year=None,
        height=None,
        fav_cuisine=None,
        fav_colour=None,
        fav_school_subject=None,
        political=None,
        religious=None,
        family_oriented=None,
        is_public=True
    ):

        self.user_id_fk = user_id_fk
        self.description = description
        self.parish = parish
        self.biography = biography
        self.sex = sex
        self.race = race
        self.birth_year = birth_year
        self.height = height
        self.fav_cuisine = fav_cuisine
        self.fav_colour = fav_colour
        self.fav_school_subject = fav_school_subject
        self.political = political
        self.religious = religious
        self.family_oriented = family_oriented
        self.is_public = is_public

    @property
    def gender(self):
        return self.sex

    @property
    def age(self):
        if self.birth_year:
            return datetime.now().year - self.birth_year
        return None

    @property
    def date_of_birth(self):
        return str(self.birth_year) if self.birth_year else None

    def __repr__(self):
        return f'<Profile {self.id} for User {self.user_id_fk}>'

    def to_dict(self):
        return {
            "id": self.id,
            "user_id_fk": self.user_id_fk,
            "description": self.description,
            "parish": self.parish,
            "biography": self.biography,
            "sex": self.sex,
            "gender": self.gender,
            "race": self.race,
            "birth_year": self.birth_year,
            "date_of_birth": self.date_of_birth,
            "age": self.age,
            "height": self.height,
            "fav_cuisine": self.fav_cuisine,
            "fav_colour": self.fav_colour,
            "fav_school_subject": self.fav_school_subject,
            "political": self.political,
            "religious": self.religious,
            "family_oriented": self.family_oriented,

            # OPTIONAL FEATURE
            "is_public": self.is_public,

            "interests": [
                interest.name for interest in self.interests
            ],
            "name": self.user.name if self.user else None,
            "photo": self.user.photo if self.user and self.user.photo else None,
        }

class Favourite(db.Model):
    __tablename__ = 'favourites'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id_fk = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    fav_user_id_fk = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __init__(self, user_id_fk, fav_user_id_fk):
        self.user_id_fk = user_id_fk
        self.fav_user_id_fk = fav_user_id_fk
    
    def __repr__(self):
        return f'<Favourite {self.id}: User {self.user_id_fk} -> User {self.fav_user_id_fk}>'
    
class BlockedUser(db.Model):
    __tablename__ = 'blocked_users'

    id = db.Column(db.Integer, primary_key=True)

    blocker_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id'),
        nullable=False
    )

    blocked_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id'),
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    def __repr__(self):
        return f'<BlockedUser {self.blocker_id} blocked {self.blocked_id}>'

class Message(db.Model):
    __tablename__ = 'messages'

    id = db.Column(db.Integer, primary_key=True)

    sender_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id'),
        nullable=False
    )

    receiver_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id'),
        nullable=False
    )

    content = db.Column(
        db.Text,
        nullable=False
    )

    timestamp = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    sender = db.relationship(
        'User',
        foreign_keys=[sender_id],
        backref='sent_messages'
    )

    receiver = db.relationship(
        'User',
        foreign_keys=[receiver_id],
        backref='received_messages'
    )

    def to_dict(self):
        return {
            "id": self.id,
            "sender_id": self.sender_id,
            "receiver_id": self.receiver_id,
            "content": self.content,
            "timestamp": self.timestamp.isoformat()
        }


class Pass(db.Model):
    __tablename__ = 'passes'

    id = db.Column(db.Integer, primary_key=True)
    user_id_fk = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    passed_user_id_fk = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, user_id_fk, passed_user_id_fk):
        self.user_id_fk = user_id_fk
        self.passed_user_id_fk = passed_user_id_fk

    def __repr__(self):
        return f'<Pass {self.user_id_fk} passed {self.passed_user_id_fk}>'

