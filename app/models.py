from hashlib import md5
from time import time
from datetime import datetime
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


class Teachers(UserMixin, db.Model):
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
        return Teachers.query.get(id)


@login.user_loader
def load_user(id):
    return Teachers.query.get(int(id))


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
    id = db.Column(db.Integer, primary_key=True)
    student_ID = db.Column(db.Integer, db.ForeignKey('students.id'))
    teacher_ID = db.Column(db.Integer, db.ForeignKey('teachers.id'))
    start_date = db.Column(db.DateTime, nullable=False)
    start_time = db.Column(db.String(10), index=True, nullable=False)
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

#     @classmethod
#     def after_commit(cls, session):
#         for obj in session._changes['add']:
#             # if recurring do this: else do nothing
#             lession_ID = obj.id
#             recurring_type = obj.recurring_radio
#             start_date = obj.start_date
#         session._changes = None
#         # get recurring type id
#         recurring_type_id = Recurring_type.query.filter_by(
#             recurring_type=recurring_type).first()
#         # get day of week for start_date
#         calendar.weekday(start_date)
#         # insert record in recurring_pattern table with lesson_ID
#         # perform separation_count math on day_of_week or whatever


# db.event.listen(db.session, 'before_commit', Lessons.before_commit)
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
    separation_count = db.Column(db.Integer())
    max_occurrences = db.Column(db.Integer())
    day_of_week = db.Column(db.Integer())
    week_of_month = db.Column(db.Integer())
    day_of_month = db.Column(db.Integer())


class Recurring_type(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    recurring_type = db.Column(db.String(15))
