from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, PasswordField, SubmitField, TextAreaField, DateField, RadioField, RadioField, BooleanField, SelectField, SelectMultipleField,EmailField
from wtforms.validators import DataRequired, StopValidation
from wtforms.widgets import CheckboxInput, ListWidget
from datetime import datetime

# This is the Registration form for the IT Department Users

class RegisterForm(FlaskForm):
    Univ_ID = StringField('SCSU ID', validators=[DataRequired()], render_kw={"Placeholder" : "SCSU ID"})
    Birth_Date = DateField('Birth Date',validators=[DataRequired()], render_kw={"placeholder": "Birth Date"})
    First_Name = StringField('First Name: ',validators=[DataRequired()], render_kw={"placeholder" : "First Name"})
    Last_Name = StringField('Last Name: ',validators=[DataRequired()], render_kw={"placeholder" : "Last Name"})
    email = EmailField('Email: ',validators=[DataRequired()], render_kw={"placeholder" : "Email"})
    user_name = StringField('Username', validators=[DataRequired()], render_kw={"placeholder": "Username"})
    user_password = PasswordField('Password', validators=[DataRequired()],  render_kw={"placeholder": "Password"})
    submit = SubmitField('Register') 


class LoginForm(FlaskForm):
    user_name = StringField('Username', validators=[DataRequired()], render_kw={"placeholder": "Username"})
    password = PasswordField('Password', validators=[DataRequired()],  render_kw={"placeholder": "Password"})
    submit = SubmitField('Login')


# Reset form will need two forms of Identification to reset passwords both birthday and University ID are required
class ResetForm(FlaskForm):
    user_name = StringField('Username', validators=[DataRequired()], render_kw={"placeholder": "Username"})
    Univ_ID = StringField('SCSU ID', validators=[DataRequired()], render_kw={"Placeholder" : "SCSU ID"})
    Birth_Date = DateField('Birth Date',validators=[DataRequired()], render_kw={"placeholder": "Birth Date"})
    email = EmailField('Email', validators=[DataRequired()])
    submit = SubmitField(label='Confirm Identity')

class ResetPassword(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()], render_kw={"placeholder": "Password"})
    confirmPassword = PasswordField('Confirm Password', validators=[DataRequired()], render_kw={"placeholder": "Confirm Password"})
    submit = SubmitField('Reset Password')



class LoanForm(FlaskForm):
    barcode = StringField('Barcode', validators=[DataRequired()])
    Equipment_Model = StringField('Equipment Model', validators=[DataRequired()])
    Equipment_Type = StringField('Equipment Type', validators=[DataRequired()])
    borrow_date = DateField('Borrow Date', validators=[DataRequired()])
    return_date = DateField('Return Date', validators=[DataRequired()])
    faculty_name = StringField('Faculty Name', validators=[DataRequired()])
    faculty_email = StringField('Faculty Email', validators=[DataRequired()])
    submit = SubmitField('Record Loan')
    
class ReturnForm(FlaskForm):
    barcode = StringField('Barcode', validators=[DataRequired()])
    return_date = DateField('Return Date', validators=[DataRequired()])
    faculty_name = StringField('Faculty Name', validators=[DataRequired()])
    faculty_email = StringField('Faculty Email', validators=[DataRequired()])
    submit = SubmitField('Return Loan')