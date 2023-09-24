from flask import Flask
from dotenv import load_dotenv
from os import environ


load_dotenv('.flaskenv')
IP = environ.get('MYSQL_IP')
USERNAME = environ.get('MYSQL_USER')
PASSWORD = environ.get('MYSQL_PASS')
DB_NAME = environ.get('MYSQL_DB')
app = Flask(__name__)
app.config['SECRET_KEY'] = 'VelocIT'

DB_CONFIG_STR = f'mysql+mysqlconnector://{USERNAME}:{PASSWORD}@{IP}/{DB_NAME}'
app.config['SQLALCHEMY_DATABASE_URI'] = DB_CONFIG_STR
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]= True


db = SQLAlchemy(app)

from app import routes
