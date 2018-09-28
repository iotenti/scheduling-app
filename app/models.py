
from hashlib import md5
from time import time
from flask import current_app
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from app import db, login


# WILL NEED TO UNDERSTAND THIS SOON #
# The User class has a new posts field, that is initialized with db.relationship. 
# This is not an actual database field, but a high-level view of the relationship 
# between users and posts, and for that reason it isn't in the database diagram. 
# For a one-to-many relationship, a db.relationship field is normally defined on the "one" side, 
# and is used as a convenient way to get access to the "many". So for example, 
# if I have a user stored in u, the expression u.posts will run a database query 
# that returns all the posts written by that user. The first argument to db.relationship 
# is the model class that represents the "many" side of the relationship. This argument can be 
# provided as a string with the class name if the model is defined later in the module. 
# The backref argument defines the name of a field that will be added to the objects of the 
# "many" class that points back at the "one" object. This will add a post.author expression 
# that will return the user given a post. The lazy argument defines how the database query 
# for the relationship will be issued, which is something that I will discuss later. 

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

    def __repr__(self):
        return '<User {}>'.format(self.username)

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

class Students(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    account_ID = db.Column(db.Integer, db.ForeignKey('accounts.id'))
    teacher_ID = db.Column(db.Integer, db.ForeignKey('teachers.id'))
    attendence_ID = db.Column(db.Integer, db.ForeignKey('attendence.id'))
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    notes = db.Column(db.String(500))

class Attendence(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_ID = db.Column(db.Integer, db.ForeignKey('students.id'))
    account_ID = db.Column(db.Integer, db.ForeignKey('accounts.id'))
    was_present = db.Column(db.TIMESTAMP(50))

class Accounts(db.Model): ## NEEDS RELATIONSHIPS DEFINED ##
    id = db.Column(db.Integer, primary_key=True)
    F_name1 = db.Column(db.String(50))
    L_name1 = db.Column(db.String(50))
    cell_phone1 = db.Column(db.String(10))
    email1 = db.Column(db.String(120))
    F_name2 = db.Column(db.String(50), nullable=True)  
    L_name2 = db.Column(db.String(50), nullable=True)
    cell_phone2 = db.Column(db.String(10), nullable=True)
    email2 = db.Column(db.String(120), nullable=True)
    account_bal = db.Column(db.Float(10))
    account_credit = db.Column(db.Float(10))
    home_phone = db.Column(db.String(10), nullable=True)

class Invoices(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.Integer, db.ForeignKey('accounts.id'))
    invoice_date = db.Column(db.TIMESTAMP(50))
    invoice_total = db.Column(db.Float(10))
    payment_total = db.Column(db.Float(10))
    invoice_due_date = db.Column(db.DateTime(50))
    payment_date = db.Column(db.DateTime(50))



