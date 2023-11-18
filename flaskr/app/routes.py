from app import app
from flask import flash, render_template, redirect, url_for, request,current_app,session
from app.forms import LoginForm, RegisterForm, ResetForm, LoanForm, ResetPassword, ResetForm
from app.models import Users, Faculty, Department, Loaned_Devices
import datetime,requests,os
from datetime import datetime, timedelta
from sqlalchemy.exc import IntegrityError
from app import db, login
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mail import Mail, Message

login.login_view = "go"
savedUser = None
def getAllLoanData():
    loans = db.session.query(Loaned_Devices.barcode,Loaned_Devices.Equipment_Model,Loaned_Devices.Equipment_Type,Loaned_Devices.borrow_date,Loaned_Devices.return_date,Loaned_Devices.faculty_name,Loaned_Devices.loan_status)
    return [{
        'barcode': barcode,
        'Equipment_Model': Equipment_Model,
        'equipment_type': Equipment_Type,
        'borrow_date': borrow_date,
        'return_date': return_date,
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
    today = datetime.today().date()
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
def Notify():
    today = datetime.date.today()
    devices = db.session.query(Loaned_Devices).all()
    for device in devices:
        recipient = device.faculty_name
        recipient_email = device.faculty_email
        date = device.return_date
        datediff = (date-today).days
        #print("Datediff: ",datediff)
        days = ""
        if datediff < 0:
            print("overdue")
        else:
            if datediff == 1:
                days = "one"
            elif datediff == 3:
                days = "three"
            elif datediff == 5:
                days = 'five'
        if days:
            message = f"Hi, {recipient}. \n This is a reminder that your loan is due in {days} days. Please make sure to return it on time. \n Thanks, IT"
            subject = "Loan Reminder"
            msg = Message(subject, recipients=[recipient_email], body = message)
            mail.send(msg)

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


    
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    # Fetch existing user information from the database
    existing_users = Users.query.all()
    existing_usernames = [user.user_name for user in existing_users]
    existing_emails = [user.email for user in existing_users]
    existing_univ_ids = [user.Univ_ID for user in existing_users]

    if form.validate_on_submit():
        try:
            existing_user = Users.query.filter(
                (Users.user_name == form.user_name.data) | (Users.Univ_ID == form.Univ_ID.data) | (Users.email == form.email.data)
            ).first()

            if existing_user:
                flash("ERROR: Please use a different ID, Email, or Username")
                return render_template('register.html', form=form, existing_usernames=existing_usernames, existing_emails=existing_emails, existing_univ_ids=existing_univ_ids)

            user = Users.query.filter_by(user_name=form.user_name.data).first()

            if existing_user:
                flash("ERROR: Please use a different ID, Email, or Username")
                return render_template('register.html', form=form, existing_usernames=existing_usernames, existing_emails=existing_emails, existing_univ_ids=existing_univ_ids)

            if user:
                return render_template('register.html', form=form, msg='Username is already taken', existing_usernames=existing_usernames, existing_emails=existing_emails, existing_univ_ids=existing_univ_ids)

            if form.email.data in existing_emails:
                return render_template('register.html', form=form, msg='Email is already taken', existing_usernames=existing_usernames, existing_emails=existing_emails, existing_univ_ids=existing_univ_ids)

            if form.Univ_ID.data in existing_univ_ids:
                return render_template('register.html', form=form, msg='University ID is already taken', existing_usernames=existing_usernames, existing_emails=existing_emails, existing_univ_ids=existing_univ_ids)

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

            return redirect(url_for('go')) 

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
    setDates()
    Notify()
    return render_template('home.html',loans=loans)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('go'))


@app.route('/loans', methods=['GET','POST'])
@login_required
def request_loan():
    form = LoanForm()
    if form.validate_on_submit():
        data = {
        'barcode': form.barcode.data,
        'Equipment_Model': form.Equipment_Model.data,
        'Equipment_Type': form.Equipment_Type.data,
        'borrow_date': form.borrow_date.data,
        'return_date': form.return_date.data,
        'faculty_name': form.faculty_name.data,
        'faculty_email': form.faculty_email.data
        }
        
        teams_webhook_url = os.getenv('TEAMS_WEBHOOK_URL')
        loan_payload = create_loan_payload(data)
        
        if send_webhook(loan_payload, teams_webhook_url):
            flash('Loan Submitted Successfully Teams Notification Sent', 'success')
            print("Webhook Success: Teams Notification Sent")
            save_loan_data(data)
            schedule_reminders(data['return_date'],teams_webhook_url)
        else:
            flash('Loan Submitted Successfully Teams Notification Failed', 'warning')
            print("Webhook Error: Teams Notification Failed")
        
        return redirect(url_for('home'))
    return render_template('loan.html', form=form) 
        
def create_loan_payload(data):
    
    body_content = [
            {"type": "TextBlock", "text": f"{key}: {data[key]}"}
            for key in data.keys()
        ]

    return {
            "type": "message",
            "attachments": [
                {
                    "contentType": "application/vnd.microsoft.card.adaptive",
                    "content": {
                        "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
                        "type": "AdaptiveCard",
                        "body": [

                            {
                                "type": "TextBlock",
                                "text": "Loan Request Notification",
                                "weight":"bolder",
                                "size" : "large"
                    
                            },
                            *body_content
                        ]
                    }
                }
            ]
        }


def schedule_reminders(return_date, teams_webhook_url):
    reminder_5_days = return_date - timedelta(days=5)
    reminder_3_days = return_date - timedelta(days=3)
    reminder_1_day = return_date - timedelta(days=1)

    today = datetime.now().date()

    if today in {reminder_5_days, reminder_3_days, reminder_1_day}:  # Check if today is one of the reminder days
        reminder_payload = create_reminder_payload(today, return_date)
        send_webhook(reminder_payload, teams_webhook_url)


def create_reminder_payload(today,return_date):

    reminder_text = f"Loan Return Date Reminder: {return_date.strftime('%Y-%m-%d')}. Today: {today.strftime('%Y-%m-%d')}"
    reminder_payload = {
        "type": "message",
        "attachments": [
            {
                "contentType": "application/vnd.microsoft.card.adaptive",
                "content": {
                    "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
                    "type": "AdaptiveCard",
                    "body": [
                        {
                            "type": "TextBlock",
                            "text": reminder_text,
                            "size": "medium",
                            "weight": "bolder"
                        }
                    ]
                }
            }
        ]
    }
    return reminder_payload
    

def send_webhook(payload, teams_webhook_url):
    
    try:

        headers = {'Content-Type': 'application/json'}

        response = requests.post(teams_webhook_url,
                                 json=payload,
                                 headers=headers)
        
        if response.status_code == 200:
            print("Webhook Success: Teams Notification Sent")
            print("Response Content:", response.content)  # Log the response content for further inspection
            return True
        else:
            print("Webhook Error: Teams Notification Failed")
            print("Response Content:", response.content)  # Log the response content for further inspection
            return False
    
    except Exception as e:
        print(f"Webhook Error: {str(e)}")
        return False

def save_loan_data(data):    
    
    deviceLoan = Loaned_Devices(
            barcode=data['barcode'],
            Equipment_Model=data['Equipment_Model'],
            Equipment_Type=data['Equipment_Type'],
            borrow_date=data['borrow_date'],
            return_date=data['return_date'],
            faculty_name=data['faculty_name'],
            faculty_email=data['faculty_email']
        )
        db.session.add(deviceLoan)
        db.session.commit()
        setDates()
        Notify()
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