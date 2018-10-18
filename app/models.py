
from hashlib import md5
from time import time
from flask import current_app
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from app import db, login


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
    notes = db.Column(db.String(500))
    # add admin field
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
        except:
            return
        return Teachers.query.get(id)


@login.user_loader
def load_user(id):
    return Teachers.query.get(int(id))


class Instruments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    instrument = db.Column(db.String(50))
    # make form to add instruments in admin section

    def __repr__(self):
        return '{}'.format(self.instrument)


class Students(db.Model):  # needs key constraints, I think
    id = db.Column(db.Integer, primary_key=True)
    account_ID = db.Column(db.Integer, db.ForeignKey('accounts.id'))
    teacher_ID = db.Column(db.Integer, db.ForeignKey('teachers.id'))
    attendence_ID = db.Column(db.Integer, db.ForeignKey('attendence.id'))
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    instrument = db.Column(db.String(50))
    notes = db.Column(db.String(500))
    # add bool archive col

    def __repr__(self):
        return '{} {} - {}'.format(
                                    self.first_name,
                                    self.last_name,
                                    self.instrument)


class Accounts(db.Model):  # needs key constrains
    id = db.Column(db.Integer, primary_key=True)
    f_name1 = db.Column(db.String(50))
    l_name1 = db.Column(db.String(50))
    cell_phone1 = db.Column(db.String(10))
    email1 = db.Column(db.String(120))
    home_phone1 = db.Column(db.String(10), nullable=True)
    f_name2 = db.Column(db.String(50), nullable=True)
    l_name2 = db.Column(db.String(50), nullable=True)
    cell_phone2 = db.Column(db.String(10), nullable=True)
    email2 = db.Column(db.String(120), nullable=True)
    account_bal = db.Column(db.Float(10))
    account_credit = db.Column(db.Float(10))
    home_phone2 = db.Column(db.String(10), nullable=True)
    # add bool archive col

    def __repr__(self):
        str = '{} {}'.format(
            self.f_name1,
            self.l_name1)

        return str

    @classmethod
    def view_all_accounts(cls):
        accounts = Accounts.query.order_by(Accounts.l_name1).all()
        return accounts

    @classmethod
    def get_alphabet(cls, accounts):
        abc = [account.l_name1[:1].upper() for account in accounts]
        abc = set(abc)
        abc = sorted(abc)

        return abc


class Attendence(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_ID = db.Column(db.Integer, db.ForeignKey('students.id'))
    account_ID = db.Column(db.Integer, db.ForeignKey('accounts.id'))
    was_present = db.Column(db.TIMESTAMP(50))
    #  Maybe make this an association table


class Invoices(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.Integer, db.ForeignKey('accounts.id'))
    invoice_date = db.Column(db.TIMESTAMP(50))
    invoice_total = db.Column(db.Float(10))
    payment_total = db.Column(db.Float(10))
    invoice_due_date = db.Column(db.DateTime(50))
    payment_date = db.Column(db.DateTime(50))


