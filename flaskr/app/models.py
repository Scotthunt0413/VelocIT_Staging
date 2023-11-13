from app import db, login
from flask_login import UserMixin
from sqlalchemy.orm import declarative_base, relationship
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import Column, ForeignKey, Integer, Table

# Define the DB Schema
class Users(UserMixin, db.Model):
    __tablename__ = 'Users'
    id = db.Column(db.Integer, primary_key=True)
    First_Name = db.Column(db.String(32), unique=False, nullable=False)
    #last name is NOT unique
    Last_Name = db.Column(db.String(64), unique=False, nullable=False)
    Univ_ID = db.Column(db.String(10), unique=True, nullable=False)
    Birth_Date = db.Column(db.DATE, unique=False, nullable=False)
    email = db.Column(db.String(64), unique=True, nullable=False)
    user_name = db.Column(db.String(255), unique=True, nullable=False)
    user_password = db.Column(db.String(255), unique=True, nullable=False)

    def set_password(self, user_password):
        # Store hashed (encrypted) password in database
        self.user_password = generate_password_hash(user_password)
    def check_password(self, user_password):
        return check_password_hash(self.user_password, user_password)
    
class Faculty(db.Model):
    __tablename__ = 'Faculty'
    Faculty_ID = db.Column(db.Integer, unique=True,nullable=False, primary_key=True)
    faculty_name = db.Column(db.String(255), unique=True,nullable=False)
    Department_ID = db.Column(db.Integer, unique=True, nullable=False)

class Department(db.Model):
    __tablename__ = 'Department'
    Department_ID = db.Column(db.Integer, unique=True,nullable=False, primary_key=True)
    Building = db.Column(db.String(255), unique=True,nullable=False)
    Room_Number = db.Column(db.Integer, unique=True, nullable=False)

class Loaned_Devices(db.Model):
    __tablename__ = 'Loaned_Devices'
    #we do not need serial #'s anymore
    barcode = db.Column(db.Integer, unique=True, nullable=False)
    Equipment_Model = db.Column(db.String(255), nullable=False)
    Equipment_Type = db.Column(db.String(255), nullable=False)
    return_date = db.Column(db.DATE, unique=False, nullable=False)
    takeout_date = db.Column(db.DATE, unique=False, nullable=False)
    faculty_name = db.Column(db.String(255), nullable=True)
    loan_status = db.Column(db.String(255),nullable=True)
    
@login.user_loader
def load_user(id):
    return db.session.query(Users).get(int(id))