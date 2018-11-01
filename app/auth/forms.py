from flask_wtf import FlaskForm
from flask import request
from wtforms import StringField, PasswordField, \
    BooleanField, SubmitField, TextAreaField
from wtforms.validators import ValidationError, \
    DataRequired, Email, EqualTo, Regexp
from app.models import Teachers
import phonenumbers


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Sign In')


class TeacherRegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    phone_num = StringField('Phone Number', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])
    state = StringField('State', validators=[DataRequired()])
    zipcode = StringField('Zip Code', validators=[DataRequired()])
    is_admin = BooleanField('Administrator')
    notes = TextAreaField('Notes', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
                            'Repeat Password',
                            validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Add Teacher')

    def validate_username(self, username):
        teacher = Teachers.query.filter_by(username=username.data).first()
        if teacher is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        teacher = Teachers.query.filter_by(email=email.data).first()
        if teacher is not None:
            raise ValidationError('Please use a different email address.')

    def validate_phone_num(form, field):
        if field.data is "":
            pass
        if len(field.data) > 16:
            raise ValidationError('Invalid phone number')
        try:
            input_number = phonenumbers.parse(field.data)
            if not (phonenumbers.is_valid_number(input_number)):
                raise ValidationError('Invalid phone number.')
        except:  # noqa: E722
            input_number = phonenumbers.parse("+1" + field.data)
            if not (phonenumbers.is_valid_number(input_number)):
                raise ValidationError('Invalid phone number.')


class EditTeacherForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    phone_num = StringField('Phone Number', validators=[
        DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    address = StringField('Address', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])
    state = StringField('State', validators=[DataRequired()])
    zipcode = StringField('Zip Code', validators=[DataRequired()])
    is_admin = BooleanField('Administrator')
    notes = TextAreaField('Notes', validators=[DataRequired()])
    submit = SubmitField('Add Teacher')

    def __init__(self, original_email, original_username, original_phone_num, *args, **kwargs):
        super(EditTeacherForm, self).__init__(*args, **kwargs)
        self.original_email = original_email
        self.original_username = original_username
        # So <input> can be used in html for better messaging
        if request.method == 'GET':
            self.phone_num.data = original_phone_num
        if request.method == 'POST':
            self.phone_num.data = self.phone_num.data

    def validate_phone_num(form, field):
        if field.data is "":
            pass
        if len(field.data) > 16:
            raise ValidationError('Invalid phone number')
        try:
            input_number = phonenumbers.parse(field.data)
            if not (phonenumbers.is_valid_number(input_number)):
                raise ValidationError('Invalid phone number.')
        except:  # noqa: E722
            input_number = phonenumbers.parse("+1" + field.data)
            if not (phonenumbers.is_valid_number(input_number)):
                raise ValidationError('Invalid phone number.')

    def validate_username(self, username):
        teacher = Teachers.query.filter_by(username=username.data).first()
        if teacher is not None and teacher.username != self.original_username:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        teacher = Teachers.query.filter_by(email=email.data).first()
        if teacher is not None and teacher.email != self.original_email:
            raise ValidationError('Please use a different email address.')