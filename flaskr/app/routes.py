
from flask import render_template, redirect, url_for, request
from app import app
from app.forms import LoginForm, RegisterForm, ResetForm
#from app.forms import #RegisterForm

@app.route('/', methods=['GET','POST'])
def go():
    return redirect(url_for('index'))


@app.route('/home', methods=['GET','POST'])
def index():
    return render_template('home.html')


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
        user_name = form.user_name.data
        user_password = form.user_password.data
        First_Name = form.First_Name.data
        Middle_init = ""
        if form.Middle_init.data:
            Middle_init = form.Middle_init.data
        Last_Name = form.Last_Name.data
        email = form.email.data
        bdate = form.Birth_Date.data
        uid = form.Univ_ID.data

        response = "user name: " + user_name + "\n Password: " + user_password + "\n First Name: " + First_Name + "\n Last Name: " + Last_Name + "\n Email: " + email + "\n Birth Date: " + str(bdate) + "\n SCSU ID: " + str(uid)
        if Middle_init:
            response += "\n Middle Initial: " + Middle_init
        return response
    return render_template('register.html', form = form)

