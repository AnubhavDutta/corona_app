from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length,Email,EqualTo

class newHospital(FlaskForm):
    username = StringField('Enter Username', validators=[DataRequired(), Length(min=4, max=15)])
    mail = StringField('Mail', validators=[DataRequired(), Email() ])
    password = PasswordField('Password',validators=[DataRequired() ])
    confirmpassword = PasswordField('Confirm Password',validators=[DataRequired(), EqualTo(password)])
    submit = SubmitField()

class editHospital(FlaskForm):
    totalbeds = StringField('Total Beds', validators=[DataRequired()])
    availablebeds = StringField('Available Beds', validators=[DataRequired()])
    totalICU = StringField('Total ICU Beds', validators=[DataRequired()])
    availableICU = StringField('Available ICU Beds', validators=[DataRequired()])
    doctors = StringField('Number of Doctors', validators=[DataRequired()])
    submit = SubmitField()