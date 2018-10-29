from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, Optional
from app.models import Teachers, Instruments
from wtforms_alchemy import QuerySelectField


class AddAccountForm(FlaskForm):
    f_name1 = StringField('First Name', validators=[DataRequired()])
    l_name1 = StringField('Last Name', validators=[DataRequired()])
    cell_phone1 = StringField('Cell')
    email1 = StringField('Email', validators=[DataRequired(), Email()])
    home_phone1 = StringField('Home Phone')
    f_name2 = StringField('First Name')
    l_name2 = StringField('Last Name')
    cell_phone2 = StringField('Cell')
    email2 = StringField('Email', validators=[Optional(), Email()])
    home_phone2 = StringField('Home Phone')
    submit = SubmitField('submit')
# FIGURE OUT HOW TO MAKE AT LEAST 1 PHONE NUMBER REQUIRED #


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


