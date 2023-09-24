
from flask import render_template, redirect, url_for, request
from app.forms import RegisterForm
from app import app

from app import db

#from app.forms import #RegisterForm

@app.route('/')
def go():
    return redirect(url_for('index'))


@app.route('/home', methods=['GET','POST'])
def index():
    return render_template('home.html')


@app.route('/register', methods=['GET','POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        univ_iD = form.univ_id.data
        birth_date = form.birth_date.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        email = form.email.data
        user_name = form.user_name.data
        user_password = form.user_password.data
        register = User(univ_iD=univ_iD,
                        birth_date=birth_date,
                        first_name=first_name,
                        last_name=last_name,
                        email=email,
                        user_name=user_name,
                        user_passwor=user_password)
        register.set_password(user_password)
        return redirect(url_for('index'))
    return render_template('register.html', form=form) 
        

        
