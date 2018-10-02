from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField
from wtforms.validators import ValidationError, DataRequired, Length
from app.models import Students, Teachers
from wtforms_alchemy import QuerySelectField


class AddAccountForm(FlaskForm):
    f_name1 = StringField('First Name', validators=[DataRequired()])
    l_name1 = StringField('Last Name', validators=[DataRequired()])
    cell_phone1 = StringField('Cell')
    email1 = StringField('Email')
    f_name2 = StringField('First Name')
    l_name2 = StringField('Last Name')
    cell_phone2 = StringField('Cell')
    email2 = StringField('Email')
    home_phone = StringField('Home Phone')
    submit = SubmitField('Next')
# FIGURE OUT HOW TO MAKE AT LEAST 1 PHONE NUMBER REQUIRED #


class AddStudentForm(FlaskForm):

    def get_teachers():
        return Teachers.query

    # account_ID = account
    teacher_ID = QuerySelectField('select teacher...', query_factory=get_teachers, allow_blank=False)
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    notes = TextAreaField('Notes', validators=[DataRequired()])
    submit = SubmitField('Add Student')