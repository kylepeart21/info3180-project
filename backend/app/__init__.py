from flask import Flask, Blueprint
from .config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS  # <-- import CORS

# Register blueprints
auth_bp = Blueprint('auth', __name__)

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()

app = Flask(__name__)
app.config.from_object(Config)

# Enable CORS for all domains
CORS(app)

# Initialize extensions
db.init_app(app)
migrate.init_app(app, db)
jwt.init_app(app)

app.register_blueprint(auth_bp, url_prefix='/api/auth')


@jwt.user_identity_loader
def user_identity_lookup(user):
    if isinstance(user, str):
        return user
    return str(user.id) if hasattr(user, 'id') else user

from . import views
