import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

class Config:
    DEBUG = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-here'
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///jamdate.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = "your-256-bit-secret"  
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)