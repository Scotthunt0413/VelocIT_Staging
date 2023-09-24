from app import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

# Define the DB Schema
class Users(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    Univ_ID = db.Column(db.String(32), unique=True, nullable=False)
    Birth_Date = db.Column(db.String(256), unique=False, nullable=False)
    First_Name = db.Column(db.String(32), unique=False, nullable=False)
    Last_Name = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(64), unique=True, nullable=False)
    user_name = db.Column(db.String(64), unique=True, nullable=False)
    user_password = db.Column(db.String(256), unique=True, nullable=False)

    def set_password(self, user_password):
        # Store hashed (encrypted) password in database
        self.user_password = generate_password_hash(user_password)
    def check_password(self, user_password):
        return check_password_hash(self.user_password, user_password)
    
@login.user_loader
def load_user(id):
    return db.session.query(Users).get(int(id))