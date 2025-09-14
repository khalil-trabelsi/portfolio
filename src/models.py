from .extensions import db
from datetime import datetime


class Experience(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    company = db.Column(db.String(50), nullable=False)
    role = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)


class Visitor(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ip = db.Column(db.String(50))
    user_agent = db.Column(db.String(200))
    visited_at = db.Column(db.DateTime, default=datetime.utcnow)
    description = db.Column(db.Text)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)