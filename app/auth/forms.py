from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, \
    BooleanField, SubmitField, TextAreaField
from wtforms.validators import ValidationError, \
    DataRequired, Email, EqualTo
from app.models import Teachers


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


class EditTeacherForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    phone_num = StringField('Phone Number', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])
    state = StringField('State', validators=[DataRequired()])
    zipcode = StringField('Zip Code', validators=[DataRequired()])
    is_admin = BooleanField('Administrator')
    notes = TextAreaField('Notes', validators=[DataRequired()])
    submit = SubmitField('Add Teacher')
