from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, ValidationError
from wtforms.validators import DataRequired, Email, Optional
from app.models import Teachers, Instruments, Accounts
from wtforms_alchemy import QuerySelectField
from sqlalchemy import or_
import phonenumbers


class AddAccountForm(FlaskForm):
    f_name1 = StringField('First Name', validators=[DataRequired()])
    l_name1 = StringField('Last Name', validators=[DataRequired()])
    cell_phone1 = StringField('Cell', validators=[Optional()])
    email1 = StringField('Email', validators=[DataRequired(), Email()])
    home_phone1 = StringField('Home Phone', validators=[Optional()])
    f_name2 = StringField('First Name')
    l_name2 = StringField('Last Name')
    cell_phone2 = StringField('Cell', validators=[Optional()])
    email2 = StringField('Email', validators=[Optional(), Email()])
    home_phone2 = StringField('Home Phone', validators=[Optional()])
    submit = SubmitField('submit')

    def __init__(self, original_email1, original_email2, *args, **kwargs):
        super(AddAccountForm, self).__init__(*args, **kwargs)
        self.original_email1 = original_email1
        self.original_email2 = original_email2

    def validate_email1(self, original_email1):
        # check to see if account exists
        check_email = Accounts.query.filter(
            or_(
                Accounts.email1 == self.original_email1,
                Accounts.email2 == self.original_email1)).first()
        print(check_email.email2)
        if (check_email is not None
                and check_email.email1 != self.original_email1
                or self.email1.data == check_email.email2):
            raise ValidationError('An account with the secondary email \
                address already exists.')

    def validate_email2(self, original_email2):
        # check to see if account exists
        check_email = Accounts.query.filter(
            or_(
                Accounts.email1 == self.original_email2,
                Accounts.email2 == self.original_email2)).first()

        if (check_email is not None
                and check_email.email2 != self.original_email2
                or self.email2.data == check_email.email1):
            raise ValidationError('An account with the secondary email \
                address already exists.')

    def validate_cell_phone1(form, field):
        if field.data is "":
            pass
        if len(field.data) > 16:
            raise ValidationError('Invalid phone number')
        try:
            input_number = phonenumbers.parse(field.data)
            if not (phonenumbers.is_valid_number(input_number)):
                raise ValidationError('Invalid phone number.')
        except:
            input_number = phonenumbers.parse("+1" + field.data)
            if not (phonenumbers.is_valid_number(input_number)):
                raise ValidationError('Invalid phone number.')

    def validate_cell_phone2(form, field):
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

    def validate_home_phone1(form, field):
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

    def validate_home_phone2(form, field):
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


class AttendenceForm(FlaskForm):
    check_in = SubmitField('Check In')
    checked_in = SubmitField('Checked In')


