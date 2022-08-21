from flask_wtf import FlaskForm
from flask import flash
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import InputRequired, Length, EqualTo, ValidationError


def validate_phone(form, field):
    if len(field.data) > 10 or len(field.data) < 7:
        flash('Phone number must be either 7 or 10 digits.', 'danger')
        raise ValidationError('Phone number must be either 7 or 10 digits.')
    elif len(field.data) == 8 or len(field.data) == 9:
        flash('Phone number must be either 7 or 10 digits.', 'danger')
        raise ValidationError('Phone number must be either 7 or 10 digits.')

class RegisterForm(FlaskForm):
    first_name = StringField('First Name', validators=[InputRequired()])
    last_name = StringField('Last Name', validators=[InputRequired()])
    phone_number = StringField('Phone number', validators=[InputRequired(), validate_phone])
    address = StringField('Street Address', validators=[InputRequired()])
    city = StringField('City', validators=[InputRequired()])
    state = SelectField('State', choices=['Select', 'AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 
        'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 
        'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY'], validators=[InputRequired()])
    zip_code = StringField('Zip Code', validators=[InputRequired(), Length(min=5, max=5)])
    submit = SubmitField()

    

class SignUpForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired()])
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    confirm_pass = PasswordField('Confirm Password', validators=[InputRequired(), EqualTo('password')])
    submit = SubmitField()

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    submit = SubmitField()