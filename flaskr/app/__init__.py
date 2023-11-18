from flask import Flask
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_mail import Mail, Message

app = Flask(__name__)
app.config['SECRET_KEY'] = 'VelocIT'

from os import environ


# force loading of environment variables

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

bootstrap = Bootstrap(app)

mail = Mail(app)

moment = Moment(app)

app.config.update(
        MAIL_SERVER = 'smtp.gmail.com',
        MAIL_PORT = 465,
        MAIL_USE_TLS = False,
        MAIL_USE_SSL = True, 
        MAIL_USERNAME = 'ij4.cheung@gmail.com',
        MAIL_PASSWORD = environ.get('MAIL_PASSWORD'),
        MAIL_DEFAULT_SENDER = ('Ian Cheung', 'ij4.cheung@gmail.com'),
        SECRET_KEY = 'abc')

from app import routes
