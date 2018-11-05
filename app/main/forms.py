from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, ValidationError, \
    BooleanField
from wtforms.validators import DataRequired, Email, Optional
from wtforms.fields.html5 import DateField
from app.models import Teachers, Instruments, Accounts
from wtforms_alchemy import QuerySelectField
from sqlalchemy import or_
import phonenumbers
from flask import request


class AddAccountForm(FlaskForm):
    primary_fname = StringField('First Name', validators=[DataRequired()])
    primary_lname = StringField('Last Name', validators=[DataRequired()])
    primary_cell_phone = StringField('Cell', validators=[Optional()])
    primary_email = StringField('Email', validators=[DataRequired(), Email()])
    primary_home_phone = StringField('Home Phone', validators=[Optional()])
    secondary_fname = StringField('First Name')
    secondary_lname = StringField('Last Name')
    secondary_cell_phone = StringField('Cell', validators=[Optional()])
    secondary_email = StringField('Email', validators=[Optional(), Email()])
    secondary_home_phone = StringField('Home Phone', validators=[Optional()])
    submit = SubmitField('submit')

    def __init__(
                self,
                original_primary_email,
                original_secondary_email,
                edit,
                *args,
                **kwargs):
        super(AddAccountForm, self).__init__(*args, **kwargs)
        if edit:
            self.edit = True
            self.original_primary_email = original_primary_email
            self.original_secondary_email = original_secondary_email
        else:
            self.edit = False

        if request.method == 'GET':
            if self.primary_cell_phone.data is not None:
                self.primary_cell_phone.data = self.primary_cell_phone.data
            else:
                self.primary_cell_phone.data = ""

            if self.primary_home_phone.data is not None:
                self.primary_home_phone.data = self.primary_home_phone.data
            else:
                self.primary_home_phone.data = ""

            if self.secondary_cell_phone.data is not None:
                self.secondary_cell_phone.data = self.secondary_cell_phone.data
            else:
                self.secondary_cell_phone.data = ""

            if self.secondary_home_phone.data is not None:
                self.secondary_home_phone.data = self.secondary_home_phone.data
            else:
                self.secondary_home_phone.data = ""

        elif request.method == 'POST':
            if self.primary_cell_phone.data is not None:
                self.primary_cell_phone.data = self.primary_cell_phone.data

            if self.primary_home_phone.data is not None:
                self.primary_home_phone.data = self.primary_home_phone.data

            if self.secondary_cell_phone.data is not None:
                self.secondary_cell_phone.data = self.secondary_cell_phone.data

            if self.secondary_home_phone.data is not None:
                self.secondary_home_phone.data = self.secondary_home_phone.data

    def validate_primary_email(self, original_primary_email):
        # if editing
        if self.edit:
            # check both email rows against provided email
            check_email = Accounts.query.filter(
                or_(
                    Accounts.primary_email == self.primary_email.data,
                    Accounts.secondary_email == self.primary_email.data)
                    ).first()
            # if email is taken, but not by this account
            if (check_email is not None
                    and check_email.primary_email
                    != self.original_primary_email):
                raise ValidationError('An account with the this email \
                    address already exists.')
        # if inserting
        elif self.edit is False:
            # check to see if account exists
            check_email = Accounts.query.filter(
                or_(
                    Accounts.primary_email == self.primary_email.data,
                    Accounts.secondary_email == self.primary_email.data)
                    ).first()
            # if so raise error
            if check_email is not None:
                raise ValidationError('An account with the this email \
                    address already exists.')

    def validate_secondary_email(self, original_secondary_email):
        # check to see if account exists
        if self.edit:
            check_email = Accounts.query.filter(
                or_(
                    Accounts.primary_email == self.secondary_email.data,
                    Accounts.secondary_email == self.secondary_email.data)
                    ).first()
            if (check_email is not None
                    and check_email.secondary_email !=
                    self.original_secondary_email):
                raise ValidationError('An account with the this email \
                    address already exists.')
        elif self.edit is False:
            check_email = Accounts.query.filter(
                or_(
                    Accounts.primary_email == self.secondary_email.data,
                    Accounts.secondary_email == self.secondary_email.data)
                    ).first()
            if check_email is not None:
                raise ValidationError('An account with the this email \
                    address already exists.')

    def validate_primary_cell_phone(form, field):
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

    def validate_secondary_cell_phone(form, field):
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

    def validate_primary_home_phone(form, field):
        # if blank, pass
        if field.data is "":
            pass
        # check length
        if len(field.data) > 16:
            raise ValidationError('Invalid phone number')
        try:
            # parse data with phonenumbers extention
            input_number = phonenumbers.parse(field.data)
            if not (phonenumbers.is_valid_number(input_number)):
                raise ValidationError('Invalid phone number.')
        except:  # noqa: E722
            # parse data with phonenumbers extention with 1
            input_number = phonenumbers.parse("+1" + field.data)
            if not (phonenumbers.is_valid_number(input_number)):
                raise ValidationError('Invalid phone number.')

    def validate_secondary_home_phone(form, field):
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


class AddStudentForm(FlaskForm):

    def get_teachers():
        return Teachers.query

    def get_instruments():
        return Instruments.query

    first_name = StringField(
                            'First Name',
                            render_kw={"placeholder": "First Name"},
                            validators=[DataRequired()])
    last_name = StringField(
                            'Last Name',
                            render_kw={"placeholder": "Last Name"},
                            validators=[DataRequired()])
    instrument = QuerySelectField(
                                'Select Instrument...',
                                query_factory=get_instruments,
                                allow_blank=False,
                                validators=[DataRequired()])
    teacher_ID = QuerySelectField(
                                'Select Teacher...',
                                query_factory=get_teachers,
                                allow_blank=False,
                                validators=[DataRequired()])
    notes = TextAreaField(
                        'Notes',
                        render_kw={'placeholder': 'Notes'},
                        validators=[DataRequired()])
    submit = SubmitField('Add Student')


class AddInstrumentForm(FlaskForm):
    instrument = StringField('Instrument:', validators=[DataRequired()])
    submit = SubmitField('Submit')


class AttendanceForm(FlaskForm):
    check_in = SubmitField('Check In')
    checked_in = SubmitField('Checked In')


class AddLessonForm(FlaskForm):

    def get_teachers():
        return Teachers.query

    teacher_ID = QuerySelectField(
                                'Select teacher...',
                                query_factory=get_teachers,
                                allow_blank=False,
                                validators=[DataRequired()])
    start_date = DateField('Start Date', format='%Y-%m-%d')
    end_date = DateField('End Date', format='%Y-%m-%d')
    start_time = StringField('Lesson time')
    is_hour = BooleanField('Hour lesson?')
    is_recurring = BooleanField('Recurring?')
    submit = SubmitField('Submit')
