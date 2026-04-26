from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    interests = db.Column(db.String(500), default="")  # Stored as comma-separated values
    theme_preference = db.Column(db.String(10), default="light")
    activities = db.relationship('Activity', backref='user', lazy=True)

class Activity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    book_title = db.Column(db.String(200), nullable=False)
    action_type = db.Column(db.String(20), nullable=False)  # 'read', 'download', 'viewed'
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
