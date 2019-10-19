from hashlib import md5
from time import time
from datetime import datetime
import calendar
from flask import current_app
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from app import db, login

# IMPORTANT LATER

# timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
# The timestamp field is going to be indexed, which is useful if you want
# to retrieve posts in chronological order. I have also added a default
# argument, and passed the datetime.utcnow function. When you pass a
# function as a default, SQLAlchemy will set the field to the value of
# calling that function (note that I did not include the () after utcnow,
# so I'm passing the function itself, and not the result of calling it).


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '{}'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            current_app.config['SECRET_KEY'],
            algorithm='HS256').decode('utf-8')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, current_app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:  # noqa: E722
            return
        return User.query.get(id)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class ContactType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    contact_type = db.Column(db.String(50))
    cancelled_Date = db.Column(db.DateTime, nullable=True)

    def __repr__(self):
        return '{}'.format(self.id)


class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    contact_type_ID = db.Column(db.Integer, db.ForeignKey('ContactType.id'))
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    address = db.Column(db.String(120))
    city = db.Column(db.String(50))
    # make a new table for state and make this stateID = db.Column(db.Integer, db.ForeignKey('State.id'))
    state = db.Column(db.String(2))
    zipcode = db.Column(db.String(5))
    notes = db.Column(db.String(500))
    is_admin = db.Column(db.Boolean, default=False, nullable=True)
    cancelled_date = db.Column(db.DateTime, nullable=True)
    primary_contact = db.Column(db.Boolean, default=False, nullable=True)


class Teachers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    phone_num = db.Column(db.String(10))
    address = db.Column(db.String(120))
    city = db.Column(db.String(50))
    state = db.Column(db.String(2))
    zipcode = db.Column(db.String(5))
    is_admin = db.Column(db.Boolean, default=False, nullable=True)
    notes = db.Column(db.String(500))
    students = db.relationship('Students', backref='teacher', lazy='dynamic')
    lessons = db.relationship('Lessons', backref='teacher', lazy='dynamic')
    # format first and last name to capitalize

    def __repr__(self):
        return '{} {}'.format(self.first_name, self.last_name)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)


class Accounts(db.Model):  # needs key constrains
    id = db.Column(db.Integer, primary_key=True)
    primary_fname = db.Column(db.String(50))
    primary_lname = db.Column(db.String(50))
    primary_cell_phone = db.Column(db.String(10))
    primary_email = db.Column(db.String(120))
    primary_home_phone = db.Column(db.String(10), nullable=True)
    secondary_fname = db.Column(db.String(50), nullable=True)
    secondary_lname = db.Column(db.String(50), nullable=True)
    secondary_cell_phone = db.Column(db.String(10), nullable=True)
    secondary_email = db.Column(db.String(120), nullable=True)
    account_bal = db.Column(db.Float(10))
    account_credit = db.Column(db.Float(10))
    secondary_home_phone = db.Column(db.String(10), nullable=True)
    students = db.relationship(
        'Students',
        backref='account',
        lazy='dynamic',
        cascade='delete')
    invoices = db.relationship('Invoices', backref='account', lazy='dynamic')

    # investigate back_populate
    # add bool archive col

    def __repr__(self):
        str = '{} {}'.format(
            self.primary_fname,
            self.primary_lname)

        return str

    # should make it's own class instead of having these functions
    # for accounts and students
    @classmethod
    def view_all_accounts(cls):
        accounts = Accounts.query.order_by(Accounts.primary_lname).all()
        return accounts

    @classmethod
    def get_account_alphabet(cls, accounts):
        abc = [account.primary_lname[:1].upper() for account in accounts]
        abc = set(abc)
        abc = sorted(abc)

        return abc


class Instruments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    instrument = db.Column(db.String(50))
    # make form to add instruments in admin section

    def __repr__(self):
        return '{}'.format(self.instrument)


class Attendance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_ID = db.Column(db.Integer, db.ForeignKey('students.id'))
    account_ID = db.Column(db.Integer, db.ForeignKey('accounts.id'))
    was_present = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    student = db.relationship('Students', foreign_keys=[student_ID])
    account = db.relationship('Accounts', foreign_keys=[account_ID])


class Students(db.Model):  # needs key constraints, I think
    id = db.Column(db.Integer, primary_key=True)
    account_ID = db.Column(db.Integer, db.ForeignKey('accounts.id'))
    teacher_ID = db.Column(db.Integer, db.ForeignKey('teachers.id'))
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    instrument = db.Column(db.String(50))
    notes = db.Column(db.String(500))
    lesson = db.relationship('Lessons', backref='student', lazy='dynamic')
    # add bool archive col

    @classmethod
    def view_all_students(cls):
        students = Students.query.order_by(Students.first_name).all()
        return students

    @classmethod
    def get_student_alphabet(cls, students):
        abc = [student.first_name[:1].upper() for student in students]
        abc = set(abc)
        abc = sorted(abc)

        return abc

    def __repr__(self):
        return '{} {} - {}'.format(
            self.first_name,
            self.last_name,
            self.instrument)


class Invoices(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.Integer, db.ForeignKey('accounts.id'))
    invoice_date = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    invoice_total = db.Column(db.Float(10))
    payment_total = db.Column(db.Float(10))
    invoice_due_date = db.Column(db.DateTime(50))
    payment_date = db.Column(db.DateTime(50))


class Lessons(db.Model):  # add relationships
    # datetimes will be stored in UTC
    # times will be stored as a datetime with a zero date
    # dates will be stored as a datetime with a zero time
    # consider this stuff ^^
    id = db.Column(db.Integer, primary_key=True)
    student_ID = db.Column(db.Integer, db.ForeignKey('students.id'))
    teacher_ID = db.Column(db.Integer, db.ForeignKey('teachers.id'))
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=True)
    start_time = db.Column(db.String(10), index=True, nullable=False)
    end_time = db.Column(db.String(10), nullable=True)
    is_hour = db.Column(db.Boolean, default=False, nullable=False)
    is_recurring = db.Column(db.Boolean, default=True, nullable=False)
    created_by = db.Column(db.String(50))
    created_date = db.Column(db.DateTime, default=datetime.utcnow)

    @classmethod
    def before_commit(cls, session):
        session._changes = {
            'add': list(session.new),
            'update': list(session.dirty),
            'delete': list(session.deleted)
        }

    # @classmethod
    # def after_commit(cls, session):

    #     for obj in session._changes['add']:
    #         lesson_ID = obj.id
    #         recurring_type = obj.recurring_radio
    #         start_date = obj.start_date
    #         recurring = obj.is_recurring
    #     session._changes = None
    #     if recurring is True:
    #         # get recurring type id
    #         recurring_type_id = Recurring_type.query.filter_by(
    #             recurring_type=recurring_type).first()
    #         # get day of week for start_date
    #         year = int(obj.start_date.strftime('%Y'))
    #         month = int(obj.start_date.strftime('%m'))
    #         day = int(obj.start_date.strftime('%d'))
    #         day_of_week = calendar.weekday(year, month, day)
    #         day_of_week = Week_days.query.filter_by(cal_ID=day_of_week).first()
    #         # store separation_count
    #         if recurring_type == 'weekly':
    #             separation_count = 1
    #         elif recurring_type == 'bi-weekly':
    #             separation_count = 2
    #         elif recurring_type == 'monthly':
    #             separation_count = 1
    #         # get day of the month
    #         day_of_month = start_date.strftime('%d')
    #         # get max occurrences
    #         # NEEDS TO BE DONE STILL

    #         # insert record in recurring_pattern table
    #         recurring_pattern = Recurring_pattern(
    #             lession_ID=lesson_ID,
    #             recurring_type_id=recurring_type_id.id,
    #             max_occurrences=3,
    #             separation_count=separation_count,
    #             day_of_week_ID=day_of_week.id,
    #             day_of_month=day_of_month
    #         )
    #         db.session.add(recurring_pattern)
    #         db.session.commit()
    #     else:
    #         pass


db.event.listen(db.session, 'before_commit', Lessons.before_commit)
# db.event.listen(db.session, 'after_commit', Lessons.after_commit)


class Recurring_pattern(db.Model):
    lesson_ID = db.Column(
        db.Integer,
        db.ForeignKey('lessons.id'),
        primary_key=True,
        autoincrement=False)
    recurring_type_id = db.Column(
        db.Integer,
        db.ForeignKey('recurring_type.id'))
    max_occurrences = db.Column(db.Integer, nullable=True)
    separation_count = db.Column(db.Integer)
    day_of_week_ID = db.Column(db.Integer,
                               db.ForeignKey('week_days.id'))
    day_of_month = db.Column(db.String(2))


class Week_days(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cal_ID = db.Column(db.Integer())
    day_of_week = db.Column(db.String(2))
    day = db.relationship('Recurring_pattern', backref='day', lazy='dynamic')

    def __repr__(self):
        return self.day_of_week


class Recurring_type(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    recurring_type = db.Column(db.String(15))
