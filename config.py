import os
from dotenv import load_dotenv

# Load .env file
load_dotenv(override=True)


class Config:
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.getenv("SECRET_KEY")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = "src/assets/"
    SERVE_STATIC_FOLDER = os.path.abspath("src/assets")
    ALGORITHM = "HS256"