from flask import render_template, flash, redirect, url_for, request, g, \
    jsonify, current_app
from flask_login import current_user, login_required
from app import db
from app.models import Teachers, Accounts, Students
from app.main import bp
from app.main.forms import AddAccountForm, AddStudentForm
from pprint import pprint, PrettyPrinter


@bp.route('/')
@bp.route('/index')
@login_required
def index():

    teacher = Teachers.query.all()
    for teach in teacher:

        print(teach.id)
        print(teach.username)
        print(teach.email)
        print(teach.password_hash)
        print(teach.first_name)
        print(teach.last_name)
        print(teach.phone_num)
        print(teach.address)
        print(teach.zipcode)
        print(teach.city)
        print(teach.state)
        print(teach.notes)

    accounts = Accounts.query.all()
    if accounts is None:
        accounts = "hi"
        print(accounts)
    else:
        for account in accounts:
            print(account.id)
            print(account.f_name1)
            print(account.l_name1)
            print(account.cell_phone1)
            print(account.email1)
            print(account.f_name2)
            print(account.l_name2)
            print(account.cell_phone2)
            print(account.email2)
            print(account.account_bal)
            print(account.account_credit)
            print(account.home_phone)

    user = {'username': 'Miguel'}
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'This is hardcoded text. Remember that.'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('index.html', title='Home', user=user, posts=posts, teacher=teacher, accounts=accounts)


@bp.route('/sign_up', methods=['GET', 'POST'])
@login_required
def sign_up():
    form = AddAccountForm()
    # if from validates
    if form.validate_on_submit():
        # this logic is flawed. Write something better to check if an account exists later
        # check_email1 = Accounts.query.filter_by(email1=form.email1.data).first()
        # check_email2 = Accounts.query.filter_by(email2=form.email2.data).first()
        # if check_email1 or check_email2 is None:
            # no account exists, kind of... add account
            account = Accounts(
                f_name1 = form.f_name1.data,
                l_name1 = form.l_name1.data,
                cell_phone1 = form.cell_phone1.data,
                email1 = form.email1.data,
                f_name2 = form.f_name2.data,
                l_name2 = form.l_name2.data,
                cell_phone2 = form.cell_phone2.data,
                email2 = form.email2.data,
                home_phone = form.home_phone.data
            )
            db.session.add(account)
            db.session.commit()
            flash('Account added!')
            # return student sign up form LATER #

            # next_page = request.args.get('next')
            # if not next_page or url_parse(next_page).netloc != '':
            #     next_page = url_for('main.index')
            # return redirect(next_page)

            return redirect(url_for('main.index'))
        # else:
        #     flash('This account already exists')
        #     return redirect(url_for('main.index')) # or somewhere more relevent
    return render_template('add_account.html', title='Sign Up', form=form)


@bp.route('/add_student', methods=['GET', 'POST'])
@login_required
def add_student():
    form = AddStudentForm()
    teachers = Teachers.query.all()
    if teachers is not None:
        Students.get_teachers_dropdown(teachers)
    else:
        flash('NO TEACHERS AROUND')

    # if for validates

    return render_template('add_student.html', title='Sign Up', form=form, teachers=teachers, account=account)