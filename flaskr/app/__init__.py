from flask import Flask
from dotenv import load_dotenv



load_dotenv('.flaskenv')




app = Flask(__name__)
app.config['SECRET_KEY'] = 'VelocIT'

from app import routes
