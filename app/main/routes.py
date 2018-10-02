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
    user = current_user

    return render_template('index.html', title='Home', user=user, students=students, instruments=instruments)


@bp.route('/sign_up', methods=['GET', 'POST'])
@login_required
def sign_up():
    form = AddAccountForm()
    # if from validates
    if form.validate_on_submit():
        # provide logic as to not duplicate account
        # provide logid to hide half of form unless second contact needed
        account = Accounts(
            f_name1=form.f_name1.data,
            l_name1=form.l_name1.data,
            cell_phone1=form.cell_phone1.data,
            email1=form.email1.data,
            f_name2=form.f_name2.data,
            l_name2=form.l_name2.data,
            cell_phone2=form.cell_phone2.data,
            email2=form.email2.data,
            home_phone=form.home_phone.data
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
    # if for validates
    if form.validate_on_submit():
        teacher = form.teacher_ID.data
        instrument = form.instrument.data
        student = Students(
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
    return render_template('add_instrument.html', title='Add An Instrument', form=form)
