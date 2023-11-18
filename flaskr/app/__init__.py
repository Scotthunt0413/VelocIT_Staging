from flask import Flask
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from os import environ
app = Flask(__name__)
from flask_mail import Mail
from flask_moment import Moment
# force loading of environment variables

load_dotenv('.flaskenv')

# Get the environment variables from .flaskenv
IP = environ.get('MYSQL_IP')
USERNAME = environ.get('MYSQL_USERNAME')
PASSWORD = environ.get('MYSQL_PASSWORD')
DB_NAME = environ.get('MYSQL_DBNAME')
SECRET_KEY = environ.get('SECRET_KEY')

app.config.update(
        MAIL_SERVER = environ.get('MAIL_SERVER'),
        MAIL_PORT = environ.get('MAIL_PORT'),
        MAIL_USE_TLS = environ.get('MAIL_USE_TLS'),
        MAIL_USE_SSL = environ.get('MAIL_USE_SSL'), 
        MAIL_USERNAME = environ.get('MAIL_USERNAME'),
        MAIL_PASSWORD = environ.get('MAIL_PASSWORD'),
        MAIL_DEFAULT_SENDER = ('IT Department', 'velocit.notifiers@gmail.com'),
        SECRET_KEY = environ.get('SECRET_KEY'))

# Specify the connection parameters/credentials for the database
DB_CONFIG_STR = f"mysql+pymysql://{USERNAME}:{PASSWORD}@{IP}/{DB_NAME}"
app.config['SQLALCHEMY_DATABASE_URI'] = DB_CONFIG_STR
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]= True
app.config['SECRET_KEY'] = SECRET_KEY

# Create database connection and associate it with the Flask application

db = SQLAlchemy(app)

login = LoginManager(app)

bootstrap = Bootstrap(app)

mail = Mail(app)

moment = Moment(app)

from app import routes