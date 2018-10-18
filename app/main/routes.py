from flask import render_template, flash, redirect, url_for, request, g, \
    jsonify, current_app
from flask_login import current_user, login_required
from app import db
from app.models import Teachers, Accounts, Students, Instruments
from app.main import bp
from app.main.forms import AddAccountForm, AddStudentForm, AddInstrumentForm


@bp.before_app_request
def before_request():
    if current_user.is_authenticated:
        g.accounts = Accounts.view_all_accounts()
        g.account_abc = Accounts.get_account_alphabet(g.accounts)
        g.students = Students.view_all_students()
        g.student_abc = Students.get_student_alphabet(g.students)


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
        flash('Account added!')
        return redirect(url_for('main.add_student', id=account.id))
        # else:
        #     flash('This account already exists')
        #     return redirect(url_for('main.index')) # or somewhere
        #     more relevent
    else:
        print("not valid")
    return render_template('add_account.html', title='Sign Up', form=form)


@bp.route('/add_student/<id>', methods=['GET', 'POST'])
@login_required
# pass account id in link - use to add student
def add_student(id):
    form = AddStudentForm()
    account = Accounts.query.get(id)
    # if for validates
    if form.validate_on_submit():

        teacher = form.teacher_ID.data
        instrument = form.instrument.data
        # add formatting so names are capitolized
        student = Students(

            account_ID=id,
            teacher_ID=teacher.id,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            instrument=instrument.instrument,
            notes=form.notes.data
        )
        db.session.add(student)
        db.session.commit()
        flash('Student added!')

        return redirect(url_for('main.add_student', id=id))

    else:
            print("not valid")

    return render_template(
                            'add_student.html',
                            title='Add Student',
                            account=account,
                            form=form)


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


@bp.route('/view_student/<id>', methods=['GET', 'POST'])
@login_required
def view_student(id):
    student = Students.query.get(id)
    return render_template(
                            'view_student.html',
                            title='Student',
                            student=student)


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
    # make casscade delete
    account = Accounts.query.get(id)
    db.session.delete(account)
    db.session.commit()

    flash('Account Deleted')
    return redirect(url_for('main.index'))

    return render_template(
                            'delete_account.html',
                            account=account,
                            title='Delete')