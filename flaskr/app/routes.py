from app import app
from flask import flash, render_template, redirect, url_for, request,current_app,session
from app.forms import LoginForm, RegisterForm, ResetForm, LoanForm, ResetPassword, ResetForm
from app.models import Users, Faculty, Department, Loaned_Devices
import datetime
import sys
from app import db, login, mail, moment, bootstrap
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mail import Mail, Message

login.login_view = "go"
savedUser = None
def getAllLoanData():
    loans = db.session.query(Loaned_Devices.barcode,Loaned_Devices.Equipment_Model,Loaned_Devices.Equipment_Type,Loaned_Devices.return_date,Loaned_Devices.takeout_date,Loaned_Devices.faculty_name,Loaned_Devices.faculty_email,Loaned_Devices.loan_status)
    return [{
        'barcode': barcode,
        'equipment_model': equipment_model,
        'equipment_type': equipment_type,
        'return_date': return_date,
        'borrow_date': borrow_date,
        'faculty_name': faculty_name,
        'faculty_email': faculty_email,
        'loan_status': loan_status
    } for(barcode, equipment_model, equipment_type, return_date, borrow_date, faculty_name, faculty_email, loan_status) in loans]

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
            db.session.query(Loaned_Devices).filter(Loaned_Devices.barcode == barcode).update({Loaned_Devices.loan_status: "overdue"})
            db.session.commit()
        else:
            db.session.query(Loaned_Devices).filter(Loaned_Devices.barcode == barcode).update({Loaned_Devices.loan_status: "not due"})
            db.session.commit()

#starting mail functionality
def sendEmails():
    today = datetime.date.today()
    devices = db.session.query(Loaned_Devices).all()
    for device in devices:
        recipient = device.faculty_name
        date = device.return_date
        if date < today-datetime.timedelta(days=1):
            print("One Day Overdue")
        if date < today-datetime.timedelta(days=3):
            print("Three Days Overdue")
        if date < today-datetime.timedelta(days=5):
            print("Five Days Overdue")

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
# def send_teams_webhook(data, html_message):
#     try:
#         teams_webhook_url = current_app.config['TEAMS_WEBHOOK_URL']

#         payload = {
#             "type" : "message", 
#             "attachments" : [
#                 {
#                     "contentType" : "text/html",
#                     "content" : html_message
#                 }
#             ]
#         }

#         headers = { 'Content-Type' : 'application/json'}

#         response = requests.post(teams_webhook_url,
#                                  json=payload,
#                                  headers=headers)
#         payload = {
#             "type" : "message", 
#             "attachments" : [
#                 {
#                     "contentType" : "text/html",
#                     "content" : html_message
#                 }
#             ]
#         }

#         headers = { 'Content-Type' : 'application/json'}

#         response = requests.post(teams_webhook_url,
#                                  json=payload,
#                                  headers=headers)

#         if response.status_code == 200:
#             return True
#         return False
#     except Exception as e:
#         return False


def request_loan():
    form = LoanForm()
    if form.validate_on_submit():
        # with open('message.html' , 'r', encoding='utf-8') as file:
        #     html_message = file.read()

        data = {
            'barcode' : form.barcode.data,
            'Equipment_Model' : form.model.data,
            'Equipment_Type' : form.type.data,
            'loan_in_date' : form.loan_in_date.data,
            'loan_date_out' : form.loan_date_out.data,
            'faculty_name' : form.faculty_name.data,
            'faculty_email': form.faculty_email.data
        }

        # if send_teams_webhook(data, html_message):
        #     flash('Loan Submitted Successfully Teams Notification Sent','success')
        # else:
        #     flash('Loan Submitted Successfully Teams Notification Failed','warning')

        
        deviceLoan = Loaned_Devices(
            barcode=data['barcode'],
            Equipment_Model=data['Equipment_Model'],
            Equipment_Type=data['Equipment_Type'],
            return_date=data['loan_in_date'],
            takeout_date=data['loan_date_out'],
            faculty_name=data['faculty_name'],
            faculty_email=data['faculty_email']
        )
        db.session.add(deviceLoan)
        db.session.commit()
        setDates()
        sendEmails()
        return redirect(url_for('home'))
    return render_template('loan.html', form=form)

@app.route('/identity', methods=['GET','POST'])
def identity():
    form = ResetForm()
    if form.validate_on_submit():
        user = db.session.query(Users).filter(Users.user_name == form.user_name.data).first()
        if user is None:
            msg = "Username Not Found"
            return render_template('verify_identity.html', form = form, msg = msg)
        if form.Birth_Date.data != user.Birth_Date:
            msg = "\nIncorrect Birth Date"
            return render_template('verify_identity.html', form = form, msg = msg)
        if form.Univ_ID.data != int(user.Univ_ID):
            msg = "\nIncorrect University ID"
            return render_template('verify_identity.html', form = form, msg = msg)
        if form.email.data != user.email:
            msg = "\nIncorrect Email"
            return render_template('verify_identity.html', form = form, msg = msg)
        global savedUser
        savedUser = user
        return redirect(url_for('reset'))
    return render_template('verify_identity.html', form = form, msg=None)

@app.route('/reset', methods=['GET','POST'])
def reset():
    form = ResetPassword()
    user = savedUser
    id = user.id
    if form.validate_on_submit():
        if form.password.data != form.confirmPassword.data:
            msg = "Passwords do not match"
            return render_template('reset_password.html', form = form, msg=msg)
        newPassword = generate_password_hash(form.password.data)
        db.session.query(Users).filter(Users.id == id).update({Users.user_password:newPassword})
        db.session.commit()
        return redirect(url_for('go'))
    return render_template('reset_password.html', form = form, msg=None)