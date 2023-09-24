
from flask import render_template, redirect, url_for, request
from app import app

from app import db

#from app.forms import #RegisterForm

@app.route('/')
def go():
    return redirect(url_for('index'))


@app.route('/home', methods=['GET','POST'])
def index():
    return render_template('home.html')

<<<<<<< HEAD

@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user_name = form.user_name.data
        password = form.password.data
        return "user name: " + user_name + "\n Password: " + password
    return render_template('forms.html', form = form)

@app.route('/register', methods=['GET','POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        univ_id = form.univ_id.data
        birth_date = form.birth_date.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        email = form.email.data
        user_name = form.user_name.data
        user_password = form.user_password.data
        register = It_User(univ_id=univ_id,
                        birth_date=birth_date,
                        first_name=first_name,
                        last_name=last_name,
                        email=email,
                        user_name=user_name,
                        user_passwor=user_password)
        register.set_password(user_password)
        return redirect(url_for('index'))
    return render_template('register.html', form=form) 
=======
>>>>>>> 1fa2100b5f19a42c9bcb2df90cd5074513d1bdda
