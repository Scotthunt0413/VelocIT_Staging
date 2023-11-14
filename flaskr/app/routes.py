from app import app

from flask import render_template, redirect, url_for, request
from app.forms import LoginForm, RegisterForm, ResetForm, LoanForm
from app.models import Users, Faculty, Department, Loaned_Devices
import datetime
import sys
from app import db, login
from flask_login import login_user, logout_user, current_user, login_required
login.login_view = "go"
def getAllLoanData():
    loans = db.session.query(Loaned_Devices.barcode,Loaned_Devices.Equipment_Model,Loaned_Devices.Equipment_Type,Loaned_Devices.return_date,Loaned_Devices.takeout_date,Loaned_Devices.faculty_name,Loaned_Devices.loan_status)
    return [{
        'serial_number': serialNumber,
        'barcode': barcode,
        'equipment_model': equipment_model,
        'equipment_type': equipment_type,
        'return_date': return_date,
        'borrow_date': borrow_date,
        'faculty_name': faculty_name,
        'loan_status': loan_status
    } for(serialNumber, barcode, equipment_model, equipment_type, return_date, borrow_date, faculty_name, loan_status) in loans]

def getSomeLoanData():
    data = db.session.query(Loaned_Devices.barcode,Loaned_Devices.loan_status)
    return [{
        'barcode': barcode,
        'loan_status': loan_status
    } for(barcode,loan_status) in data]

def setDates():
    today = datetime.date.today()
    devices = db.session.query(Loaned_Devices).all()
    for device in devices:
        date = device.return_date
        barcode = device.barcode
        if date < today:
            db.session.query(Loaned_Devices).filter(Loaned_Devices.barcode == barcode).update({Loaned_Devices.loan_status: "Overdue"})
            db.session.commit()
        else:
            db.session.query(Loaned_Devices).filter(Loaned_Devices.barcode == barcode).update({Loaned_Devices.loan_status: "Not Due"})
            db.session.commit()

@app.route('/', methods=['GET','POST'])
def go():
    data = getSomeLoanData()
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
    return render_template('login.html', form = form, data = data)


    
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


@app.route('/home')
@login_required
def home():
    loans = getAllLoanData()
    setDates()
    return render_template('home.html',loans=loans)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('go'))


@app.route('/request',methods=['GET','POST'])
@login_required
def request_loan():
    form = LoanForm()
    if form.validate_on_submit():
        print("inside the if statement",file=sys.stderr)
        deviceLoan = Loaned_Devices(
            barcode = form.barcode.data,
            Equipment_Model = form.model.data,
            Equipment_Type = form.type.data,
            loan_in_date = form.loan_in_date.data,
            loan_date_out = form.loan_date_out.data,
            faculty_name = form.faculty_name.data
        )
        db.session.add(deviceLoan)
        db.session.commit()
        setDates()
        return redirect(url_for('home'))
    return render_template('loan.html', form=form)