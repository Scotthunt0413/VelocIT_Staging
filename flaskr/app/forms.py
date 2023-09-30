from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, PasswordField, SubmitField, TextAreaField, DateField, RadioField, RadioField, BooleanField, SelectField, SelectMultipleField,EmailField
from wtforms.validators import DataRequired, StopValidation
from wtforms.widgets import CheckboxInput, ListWidget

# This is the Registration form for the IT Department Users

class RegisterForm(FlaskForm):
    Univ_ID = IntegerField('SCSU ID', validators=[DataRequired()], render_kw={"Placeholder" : "SCSU ID"})
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
    Univ_ID = IntegerField('SCSU ID', validators=[DataRequired()], render_kw={"Placeholder" : "SCSU ID"})
    Birth_Date = DateField('Birth Date',validators=[DataRequired()], render_kw={"placeholder": "Birth Date"})
    submit = SubmitField(label='Reset Password', validators=[DataRequired()])




#WE will need to readdress the loan form we want to start the login process first 
class LoanForm(FlaskForm):
   faculty = StringField('Faculty Name: ',validators=[DataRequired()])
   device = StringField('Which device do you need? ',validators=[DataRequired()])
   is_located = StringField('Device Loca ',validators=[DataRequired()])
   loan_Date_In = DateField('When will this device be deployed? ',validators=[DataRequired()])
   why = StringField('Why do you need this device? ',validators=[DataRequired()])
   submit = SubmitField('Request Loan')