from flask import render_template, flash, redirect, url_for, request, g, \
    jsonify, current_app
from flask_login import current_user, login_required
from app import db
from app.models import Teachers, Accounts, Students, Instruments
from app.main import bp
from app.main.forms import AddAccountForm, AddStudentForm, AddInstrumentForm


@bp.route('/')
@bp.route('/index')
@login_required
def index():

    instruments = Instruments.query.all()
    students = Students.query.all()
    accounts = Accounts.query.all()
    user = current_user

    return render_template(
                            'index.html',
                            title='Home',
                            user=user,
                            students=students,
                            accounts=accounts,
                            instruments=instruments)


@bp.route('/sign_up', methods=['GET', 'POST'])
@login_required
def sign_up():
    form = AddAccountForm()
    # if from validates
    if form.validate_on_submit():
        # provide logic as to not duplicate account
        # provide logid to hide half of form unless second contact needed
        # add formatting so names are capitolized
        account = Accounts(
            f_name1=form.f_name1.data,
            l_name1=form.l_name1.data,
            cell_phone1=form.cell_phone1.data,
            email1=form.email1.data,
            home_phone1=form.home_phone1.data,
            f_name2=form.f_name2.data,
            l_name2=form.l_name2.data,
            cell_phone2=form.cell_phone2.data,
            email2=form.email2.data,
            home_phone2=form.home_phone2.data
        )
        db.session.add(account)
        db.session.commit()
        # session['id'] = account.id
        # flash('Account added!')
        # account_ID = account.id

        return redirect(url_for('main.add_student'))
        # else:
        #     flash('This account already exists')
        #     return redirect(url_for('main.index')) # or somewhere
        #     more relevent
    else:
        print("not valid")
    return render_template('add_account.html', title='Sign Up', form=form)


@bp.route('/add_student', methods=['GET', 'POST'])
@login_required
def add_student():
    form = AddStudentForm()
    # if for validates
    if form.validate_on_submit():

        teacher = form.teacher_ID.data
        instrument = form.instrument.data
        account = form.account_ID.data
        # add formatting so names are capitolized
        student = Students(

            account_ID=account.id,
            teacher_ID=teacher.id,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            instrument=instrument.instrument,
            notes=form.notes.data
        )
        db.session.add(student)
        db.session.commit()
        flash('Student added!')
        return redirect(url_for('main.index'))

    return render_template('add_student.html', title='Sign Up', form=form)


@bp.route('/add_instrument', methods=['GET', 'POST'])
@login_required
def add_instrument():
    # display Instruments.query.all() on right side, make it delete/editable?
    form = AddInstrumentForm()
    if form.validate_on_submit():
        instrument = Instruments(
            instrument=form.instrument.data
        )
        db.session.add(instrument)
        db.session.commit()
        flash('Instrument added!')
        return redirect(url_for('main.add_instrument'))
    return render_template(
                            'add_instrument.html',
                            title='Add An Instrument',
                            form=form)


@bp.route('/view_all_accounts')
@login_required
def view_all_accounts():
    accounts = Accounts.query.order_by(Accounts.l_name1).all()
    abc = [
        "A", "B", "C", "D", "E",
        "F", "G", "H", "I", "J",
        "K", "L", "M"
    ]
    xyz = [
        "N", "O", "P", "Q", "R",
        "S", "T", "U", "V", "W",
        "X", "Y", "Z"
    ]
    return render_template(
                            'view_all_accounts.html',
                            title='Accounts',
                            abc=abc,
                            xyz=xyz,
                            accounts=accounts)


@bp.route('/view_account/<id>', methods=['GET', 'POST'])
@login_required
def view_account(id):
    account = Accounts.query.get(id)
    students = Students.query.filter_by(account_ID=id).all()
    # probably do a join here

    return render_template(
                            'view_account.html',
                            title='Account',
                            students=students,
                            account=account)


@bp.route('/edit_account/<id>', methods=['GET', 'POST'])
@login_required
def edit_account(id):
    account_in_db = Accounts.query.get(id)
    form = AddAccountForm()
    if form.validate_on_submit():

        account_in_db.f_name1 = form.f_name1.data
        account_in_db.l_name1 = form.l_name1.data
        account_in_db.cell_phone1 = form.cell_phone1.data
        account_in_db.email1 = form.email1.data
        account_in_db.home_phone1 = form.home_phone1.data
        account_in_db.f_name2 = form.f_name2.data
        account_in_db.l_name2 = form.l_name2.data
        account_in_db.cell_phone2 = form.cell_phone2.data
        account_in_db.email2 = form.email2.data
        account_in_db.home_phone2 = form.home_phone2.data
        db.session.commit()

        flash('Your changes have been saved.')
        return redirect(url_for('main.view_account', id=id))

    elif request.method == 'GET':

        form.f_name1.data = account_in_db.f_name1
        form.l_name1.data = account_in_db.l_name1
        form.cell_phone1.data = account_in_db.cell_phone1
        form.email1.data = account_in_db.email1
        form.home_phone1.data = account_in_db.home_phone1
        form.f_name2.data = account_in_db.f_name2
        form.l_name2.data = account_in_db.l_name2
        form.cell_phone2.data = account_in_db.cell_phone2
        form.email2.data = account_in_db.email2
        form.home_phone2.data = account_in_db.home_phone2
    return render_template(
                            'edit_account.html',
                            title='Edit Account',
                            form=form,
                            account_in_db=account_in_db)


@bp.route('/delete_account/<id>', methods=['GET', 'POST'])
@login_required
def delete_account(id):
    account = Accounts.query.get(id)
    return render_template(
                            'delete_account.html',
                            account=account,
                            title='Delete')