from app import app
from flask import render_template, redirect, url_for, request
from app.forms import LoginForm, RegisterForm, ResetForm, LoanForm, FacultyForm
from app.models import Users, Faculty, Department, Loaned_Devices
from app import db, login
from flask_login import login_user, logout_user, current_user, login_required
import csv, os, sqlite3
import pandas as pd

app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['DATABASE'] = 'csv_data.db'


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
        deviceLoan = Loaned_Devices(
            serialNumber = form.serial.data,
            barcode = form.barcode.data,
            Equipment_Model = form.model.data,
            Equipment_Type = form.type.data,
            loan_in_date = form.loan_in_date.data,
            loan_date_out = form.loan_date_out.data,
            faculty_name = form.faculty_name.data,
            faculty_email = form.faculty_email.data
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



def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() == 'csv'

@app.route('/upload')
def index():
    return render_template('upload.html')

@app.route('/upload', methods=['GET','POST'])
def upload():
    if 'file' not in request.files:
        return redirect(request.url)
    
    file = request.files['file']

    if file.filename == '':
        return redirect(request.url)

    if file and allowed_file(file.filename):
        filename = file.filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        # Parse the CSV file using pandas
        csv_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        df = pd.read_csv(csv_path)

        # Insert the DataFrame into the database
        conn = sqlite3.connect(app.config['DATABASE'])
        df.to_sql('csv_data', conn, if_exists='append', index=False)
        conn.close()

        return redirect(url_for('upload'))
    return render_template('upload.html')

@app.route('/show_csv')
def show_csv():
    conn = sqlite3.connect(app.config['DATABASE'])
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM csv_data')
    data = cursor.fetchall()
    conn.close()
    return render_template('upload.html', data=data)