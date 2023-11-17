from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, PasswordField, SubmitField, TextAreaField, DateField, RadioField, RadioField, BooleanField, SelectField, SelectMultipleField,EmailField
from wtforms.validators import DataRequired, StopValidation
from wtforms.widgets import CheckboxInput, ListWidget

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
    submit = SubmitField(label='Reset Password', validators=[DataRequired()])




#WE will need to readdress the loan form we want to start the login process first 
class LoanForm(FlaskForm):
   barcode = StringField('Barcode: ',validators=[DataRequired()])
   model = StringField('Equipment Model: ',validators=[DataRequired()])
   type = StringField('Equipment Type: ',validators=[DataRequired()])
   return_date = DateField('When will this loan be due? ',validators=[DataRequired()])
   takeout_date = DateField('When was this loan taken out? ',validators=[DataRequired()])
   faculty_name = StringField('Faculty Name: ',validators=[DataRequired()])
   facultyLocation = StringField('Faculty Location',validators=[DataRequired()])
   facultyEmail = EmailField('Faculty Email: ',validators=[DataRequired()])
   submit = SubmitField('Record Loan')