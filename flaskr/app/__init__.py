from flask import Flask
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from os import environ

app = Flask(__name__)


from os import environ


# force loading of environment variables

load_dotenv('.flaskenv')


## MIKE WANTS US TO PUT ENVIRONMENT VARIABLES OUTSIDE OF THE WORKING DIRECTORY FOR SECURTIY MEASURES
# Get the environment variables from .flaskenv
IP = environ.get('MYSQL_IP')
USERNAME = environ.get('MYSQL_USERNAME')
PASSWORD = environ.get('MYSQL_PASSWORD')
DB_NAME = environ.get('MYSQL_DBNAME')

# Specify the connection parameters/credentials for the database
DB_CONFIG_STR = f"mysql+pymysql://{USERNAME}:{PASSWORD}@{IP}/{DB_NAME}"
app.config['SQLALCHEMY_DATABASE_URI'] = DB_CONFIG_STR
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]= True
app.config['SECRET_KEY'] = 'VelocIT'


# Create database connection and associate it with the Flask application

db = SQLAlchemy(app)

login = LoginManager(app)

bootstrap = Bootstrap(app)



from app import routes
