import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "replace-with-your-secret-key"
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY") or "replace-with-your-jwt-secret"
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or "sqlite:///app.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False