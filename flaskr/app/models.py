from app import db, login
from flask_login import UserMixin
from sqlalchemy.orm import declarative_base, relationship
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import Column, ForeignKey, Integer, Table

class It_User(UserMixin, db.Model):
    __tablename__ = 'It_User'
    It_User_ID = db.Column(db.Integer, primary_key=True)
    univ_id = db.Column(db.Integer, unique=True)