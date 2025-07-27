#models.py

from datetime import datetime
from sqlalchemy.dialects.mysql import JSON  
from moneyflow.extensions import db 

class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(200))
    date = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False) 
    email = db.Column(db.String(120), unique=True)
    preferences = db.Column(JSON, nullable=True)
    profile_picture = db.Column(db.String(200))
    expenses = db.relationship('Expense', backref='user', lazy=True)
    reset_token = db.Column(db.String(100))
    reset_token_expiration = db.Column(db.DateTime)