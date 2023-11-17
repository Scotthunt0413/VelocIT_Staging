from app import app
from flask import render_template,render_template_string, redirect, url_for, request, current_app,flash
from app.forms import LoginForm, RegisterForm, ResetForm, LoanForm
from app.models import Users, Faculty, Department, Loaned_Devices
import datetime,os,json
import sys,requests
from app import db, login
from flask_login import login_user, logout_user, current_user, login_required
from sqlalchemy.exc import IntegrityError
login.login_view = "go"
def getAllLoanData():
    loans = db.session.query(Loaned_Devices.barcode,Loaned_Devices.Equipment_Model,Loaned_Devices.Equipment_Type,Loaned_Devices.return_date,Loaned_Devices.takeout_date,Loaned_Devices.faculty_name,Loaned_Devices.loan_status)
    return [{
        'barcode': barcode,
        'equipment_model': equipment_model,
        'equipment_type': equipment_type,
        'return_date': return_date,
        'borrow_date': borrow_date,
        'faculty_name': faculty_name,
        'loan_status': loan_status
    } for(barcode, equipment_model, equipment_type, return_date, borrow_date, faculty_name, loan_status) in loans]

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
        flash('An unexpected error occurred. Please try again.', 'danger')
    return render_template('register.html', form=form)


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


        data = {
            'barcode' : form.barcode.data,
            'Equipment_Model' : form.model.data,
            'Equipment_Type' : form.type.data,
            'loan_in_date' : form.loan_in_date.data,
            'loan_date_out' : form.loan_date_out.data,
            'faculty_name' : form.faculty_name.data
        }

        teams_webhook_url = os.getenv('TEAMS_WEBHOOK_URL')
        
        
        body_content = [
            {"type": "TextBlock", "text": f"{key}: {data[key]}"}
            for key in data.keys()
        ]

        loan_payload = {
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


        if send_webhook(loan_payload, teams_webhook_url):
            flash('Loan Submitted Successfully Teams Notification Sent', 'success')
            print("Webhook Success: Teams Notification Sent")
        else:
            flash('Loan Submitted Successfully Teams Notification Failed', 'warning')
            print("Webhook Error: Teams Notification Failed")

        
        deviceLoan = Loaned_Devices(
            barcode=data['barcode'],
            Equipment_Model=data['Equipment_Model'],
            Equipment_Type=data['Equipment_Type'],
            return_date=data['loan_in_date'],
            takeout_date=data['loan_date_out'],
            faculty_name=data['faculty_name']
        )
        db.session.add(deviceLoan)
        db.session.commit()
        setDates()
        
        return redirect(url_for('home'))
    return render_template('loan.html', form=form)
    

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
    



