from app import app
from flask import flash, render_template, redirect, url_for, request,current_app
from app.forms import LoginForm, RegisterForm, ResetForm, LoanForm, FacultyForm
from app.models import Users, Faculty, Department, Loaned_Devices
from app import db, login
from flask_login import login_user, logout_user, current_user, login_required
import requests
from sqlalchemy.exc import IntegrityError



login.login_view = "go"
def getAllLoanData():
    loans = db.session.query(Loaned_Devices.serialNumber, Loaned_Devices.barcode,Loaned_Devices.Equipment_Model,Loaned_Devices.Equipment_Type,Loaned_Devices.loan_in_date,Loaned_Devices.loan_date_out,Loaned_Devices.faculty_name)
    return [{
        'serial_number': serialNumber,
        'barcode': barcode,
        'equipment_model': equipment_model,
        'equipment_type': equipment_type,
        'return_date': return_date,
        'borrow_date': borrow_date,
        'faculty_name': faculty_name,
    } for(serialNumber, barcode, equipment_model, equipment_type, return_date, borrow_date, faculty_name) in loans]

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
        try:
            user = db.session.query(Users).filter_by(user_name=form.user_name.data).first()
            if user is not None:
                return render_template('register.html', form=form, msg='Username is already taken')

            if user is None:
                user = Users(
                    user_name=form.user_name.data,
                    First_Name=form.First_Name.data,
                    Last_Name=form.Last_Name.data,
                    Birth_Date=form.Birth_Date.data,
                    Univ_ID=form.Univ_ID.data,
                    email=form.email.data
                )
                user.set_password(form.user_password.data)
                db.session.add(user)
                db.session.commit()
                login_user(user)
                flash('Registration successful', 'success')
            return redirect(url_for('go'))  # Redirect to the login page ('go' route)
        
        except IntegrityError as e:
            db.session.rollback()
            if "UNIQUE constraint failed" in str(e):
                flash('Error: This username or University ID is already in use.', 'danger')
            else:
                flash('An unexpected error occurred. Please try again.', 'danger')
    return render_template('register.html', form=form)

@app.route('/home')
@login_required
def home():
    loans = getAllLoanData()
    return render_template('home.html',loans=loans)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('go'))


@app.route('/request',methods=['GET','POST'])
@login_required
def send_teams_webhook(data, html_message):
    try:
        teams_webhook_url = current_app.config['TEAMS_WEBHOOK_URL']

        payload = {
            "type" : "message", 
            "attachments" : [
                {
                    "contentType" : "text/html",
                    "content" : html_message
                }
            ]
        }

        headers = { 'Content-Type' : 'application/json'}

        response = requests.post(teams_webhook_url,
                                 json=payload,
                                 headers=headers)

        if response.status_code == 200:
            return True
        return False
    except Exception as e:
        return False


def request_loan():
    form = LoanForm()
    if form.validate_on_submit():
        with open('message.html' , 'r', encoding='utf-8') as file:
            html_message = file.read()

        data = {
            'serialNumber' : form.serial.data,
            'barcode' : form.barcode.data,
            'Equipment_Model' : form.model.data,
            'Equipment_Type' : form.type.data,
            'loan_in_date' : form.loan_in_date.data,
            'loan_date_out' : form.loan_date_out.data,
            'faculty_name' : form.faculty_name.data
        }

        if send_teams_webhook(data, html_message):
            flash('Loan Submitted Successfully Teams Notification Sent','success')
        else:
            flash('Loan Submitted Successfully Teams Notification Failed','warning')

        
        deviceLoan = Loaned_Devices(
            serialNumber=data['serial'],
            barcode=data['barcode'],
            Equipment_Model=data['model'],
            Equipment_Type=data['type'],
            loan_in_date=data['loan_in_date'],
            loan_date_out=data['loan_date_out'],
            faculty_name=data['faculty_name']
        )

        db.session.add(deviceLoan)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('loan.html', form=form)


@app.route('/faculty',methods=['GET','POST'])
@login_required
def faculty():
    form = FacultyForm()
    if form.validate_on_submit():
        faculty = Faculty(
            faculty_name = form.name.data,
            Department_ID = form.department_id.data
        )
        db.session.add(faculty)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('faculty.html', form=form)