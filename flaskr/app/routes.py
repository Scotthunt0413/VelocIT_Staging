
from flask import render_template, redirect, url_for, request
from app import app
from app.forms import LoginForm, RegisterForm, ResetForm
from app.models import Users
from app import db
from flask_login import login_user, logout_user, current_user, login_required
#from app.forms import #RegisterForm

@app.route('/', methods=['GET','POST'])
def go():
    return redirect(url_for('index'))


@app.route('/home', methods=['GET','POST'])
def index():
    name = f"Welcone{Users.First_Name}"
    return render_template('home.html')


@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user_name = form.user_name.data
        user = db.session.query(Users).filter_by(user_name=user_name).first()
        if user is None:
            form.username.data = ''
            form.password.data = ''
            return render_template('index.html', form=form, msg=f'No user found with username "{user_name}"')
        if not user.check_password(form.password.data):
            form.username.data = ''
            form.password.data = ''
            return render_template('index.html', form=form, msg=f"Incorrect Password")
        password = form.password.data
        return "user name: " + user_name + "\n Password: " + password
    return render_template('forms.html', form = form)


@app.route('/register', methods=['GET','POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        # user_name = form.user_name.data
        # user_password = form.user_password.data
        # First_Name = form.First_Name.data
        # Last_Name = form.Last_Name.data
        # email = form.email.data
        # bdate = form.Birth_Date.data
        # uid = form.Univ_ID.data

        # response = "user name: " + user_name + "\n Password: " + user_password + "\n First Name: " + First_Name + "\n Last Name: " + Last_Name + "\n Email: " + email + "\n Birth Date: " + str(bdate) + "\n SCSU ID: " + str(uid)
        # if Middle_init:
        #     response += "\n Middle Initial: " + Middle_init
        # return response
    
        user = db.session.query(Users).filter_by(user_name=form.user_name.data).first()
        if user is not None:
            return render_template('register.html',
                form=form, msg='Username is already taken')
        if user is None:
            user = Users(
                user_name = form.user_name.data,
                First_Name = form.First_Name.data,
                Last_Name = form.Last_Name.data,
                Birth_Date = form.Birth_Date.data,
                Univ_ID = form.Univ_ID.data,
                email = form.email.data
            )
            user.set_password(form.user_password.data)
            db.session.add(user)
            db.session.commit()
            login_user(user)
            msg = 'Registraton successful'
            return redirect(url_for('test'))
    return render_template('register.html', form = form)

@login_required
@app.route('/test')
def test():
    return render_template('login.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('go'))
