from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)

    # New fields for profile
    bio = db.Column(db.Text, default="")  # Optional bio
    profile_picture = db.Column(db.String(255), default="default.jpg")
    gender = db.Column(db.String(20), default="Not Specified")
    age = db.Column(db.Integer)
    location = db.Column(db.String(150), default="")

    # New role column: default to "subscriber"
    role = db.Column(db.String(50), default="subscriber")

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<User {self.username}>"