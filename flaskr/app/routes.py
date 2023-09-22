
from flask import render_template, redirect, url_for, request
from app import app
#from app.forms import #RegisterForm

@app.route('/')
def go():
    return redirect(url_for('index'))


@app.route('/home', methods=['GET','POST'])
def index():
    return render_template('home.html')

