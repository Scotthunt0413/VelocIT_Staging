
from flask import render_template, redirect, url_for, request
from app import app
from app.forms import LoginForm, RegisterForm, ResetForm, LoanForm
from app.models import Users, It_User, Loans
from app import db
from flask_login import login_user, logout_user, current_user, login_required
#from app.forms import #RegisterForm

def getAllLoanData():
    loans = db.session.query(Loans.device, Loans.faculty,Loans.why,Loans.is_located,Loans.loan_date_in)
    return [{
        'device': device,
        'faculty': faculty,
        'why': why,
        'is_located': is_located,
        'loan_date_in': loan_date_in
    } for(device, faculty, why, is_located, loan_date_in) in loans]

@app.route('/', methods=['GET','POST'])
def go():
    #Redirect authenticated users to homepage
    if current_user.is_authenticated:
        return(redirect(url_for('home')))
    form = LoginForm()
    if form.validate_on_submit():
        user_name = form.user_name.data
        user = db.session.query(Users).filter_by(user_name=user_name).first()
        if user is None:
            form.user_name.data = ''
            form.password.data = ''
            return render_template('login.html', form=form, msg=f'No user found with username "{user_name}"')
        if not user.check_password(form.password.data):
            form.user_name.data = ''
            form.password.data = ''
            return render_template('login.html', form=form, msg=f"Incorrect Password")
        login_user(user)
        return redirect(url_for('home'))
    return render_template('login.html', form = form)

@app.route('/register', methods=['GET','POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
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
            return redirect(url_for('home'))
    return render_template('register.html', form = form)

@login_required
@app.route('/home')
def home():
    loans = getAllLoanData()
    return render_template('home.html',loans=loans)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('go'))

@app.route('/request',methods=['GET','POST'])
def request_loan():
    form = LoanForm()
    if form.validate_on_submit():
        deviceLoan = Loans(
            faculty = form.faculty.data,
            device = form.device.data,
            is_located = form.is_located.data,
            loan_date_in = form.loan_Date_In.data,
            why = form.why.data
        )
        db.session.add(deviceLoan)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('loan.html', form=form)