from flask import Flask
from dotenv import load_dotenv

app = Flask(__name__)
app.config['SECRET_KEY'] = 'VelocIT'

load_dotenv('.flaskenv')


from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

from os import environ
import mysql.connector

# force loading of environment variables
from dotenv import load_dotenv

load_dotenv('.flaskenv')

# Get the environment variables from .flaskenv
IP = environ.get('MYSQL_IP')
USERNAME = environ.get('MYSQL_USERNAME')
PASSWORD = environ.get('MYSQL_PASSWORD')
DB_NAME = environ.get('MYSQL_DBNAME')

# Specify the connection parameters/credentials for the database
DB_CONFIG_STR = f"mysql+pymysql://{USERNAME}:{PASSWORD}@{IP}/{DB_NAME}"
app.config['SQLALCHEMY_DATABASE_URI'] = DB_CONFIG_STR
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]= True

# Create database connection and associate it with the Flask application
db = SQLAlchemy(app)

login = LoginManager(app)



from app import routes
