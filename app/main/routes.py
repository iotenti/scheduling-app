from flask import render_template, flash, redirect, url_for, request, g
from flask_login import current_user, login_required
from datetime import datetime, date
import calendar
from dateutil import tz
from time import strftime
from app import db
from app.models import Teachers, Accounts, Students, Instruments, Attendance, \
    Recurring_type, Lessons, Week_days
from app.main import bp
from app.main.forms import AddAccountForm, AddStudentForm, AddInstrumentForm, \
    AttendanceForm, AddLessonForm
from app.auth.forms import EditTeacherForm


@bp.before_app_request
def before_request():
    # make sure this is all appropriate. especially g.today
    if current_user.is_authenticated:
        g.accounts = Accounts.view_all_accounts()
        g.account_abc = Accounts.get_account_alphabet(g.accounts)
        g.students = Students.view_all_students()
        g.student_abc = Students.get_student_alphabet(g.students)
        g.today = datetime.utcnow()


@bp.route('/')
@bp.route('/index')
@login_required
def index():
    attendance = Attendance.query.all()
    instruments = Instruments.query.all()
    students = Students.query.all()
    accounts = Accounts.query.all()
    user = current_user
    recurring = Recurring_type.query.all()
    lessons = Lessons.query.all()
    days = Week_days.query.all()
    flash('Fix teacher admin check box')
    return render_template(
                            'index.html',
                            title='Home',
                            user=user,
                            lessons=lessons,
                            students=students,
                            accounts=accounts,
                            attendance=attendance,
                            recurring=recurring,
                            days=days,
                            instruments=instruments)


# add account
@bp.route('/sign_up', methods=['GET', 'POST'])
@login_required
def sign_up():
    h1 = 'Sign Up!'
    original_primary_email = ""
    original_secondary_email = ""
    edit = False
    form = AddAccountForm(
        original_primary_email,
        original_secondary_email,
        edit)

    # if form validates
    if form.validate_on_submit():
        # check if at least 1 phone num is given
        if (form.primary_cell_phone.data == ""
                and form.primary_home_phone.data == ""
                and form.secondary_cell_phone.data == ""
                and form.secondary_home_phone.data == ""):
            # wish I knew how to repopulate the form

            flash('Please enter a phone number')
            return redirect(url_for('main.sign_up'))

        account = Accounts(
            primary_fname=form.primary_fname.data.capitalize(),
            primary_lname=form.primary_lname.data.capitalize(),
            primary_cell_phone=form.primary_cell_phone.data,
            primary_email=form.primary_email.data,
            primary_home_phone=form.primary_home_phone.data,
            secondary_fname=form.secondary_fname.data.capitalize(),
            secondary_lname=form.secondary_lname.data.capitalize(),
            secondary_cell_phone=form.secondary_cell_phone.data,
            secondary_email=form.secondary_email.data,
            secondary_home_phone=form.secondary_home_phone.data
        )
        db.session.add(account)
        db.session.commit()
        flash('Account added!')

        return redirect(url_for('main.add_student', id=account.id))

    return render_template(
                            'add_account.html',
                            title='Sign Up',
                            h1=h1,
                            form=form)


@bp.route('/add_instrument', methods=['GET', 'POST'])
@login_required
def add_instrument():
    # display Instruments.query.all() on right side, make it delete/editable?
    form = AddInstrumentForm()
    if form.validate_on_submit():
        instrument = Instruments(
            instrument=form.instrument.data.capitalize()
        )

        db.session.add(instrument)
        db.session.commit()
        flash('Instrument added!')

        return redirect(url_for('main.add_instrument'))
    return render_template(
                            'add_instrument.html',
                            title='Add An Instrument',
                            form=form)


@bp.route('/add_lesson/<id>', methods=['GET', 'POST'])
@login_required
def add_lesson(id):
    form = AddLessonForm()
    if form.validate_on_submit():
        teacher = form.teacher_ID.data
        user = str(current_user)
        # might want to change is_hour in model to end
        # _time and store that instead, or also
        lesson = Lessons(
            student_ID=int(id),
            teacher_ID=teacher.id,
            start_date=form.start_date.data,
            start_time=form.start_time.data,
            is_hour=form.is_hour.data,
            is_recurring=form.is_recurring.data,
            created_by=user
        )
        if form.recurring_radio.data == 'weekly':
            print('week')
            lesson.is_recurring = True
        elif form.recurring_radio.data == 'bi-weekly':
            print('biweek')
            lesson.is_recurring = True
        elif form.recurring_radio.data == 'monthly':
            print('monthly')
            lesson.is_recurring = True
        elif form.recurring_radio.data == 'not_recurring':
            print(form.recurring_radio.data)
            lesson.is_recurring = False
        year = int(lesson.start_date.strftime('%Y'))
        month = int(lesson.start_date.strftime('%m'))
        day = int(lesson.start_date.strftime('%d'))
        day_of_week = calendar.weekday(year, month, day)

        # insert record in recurring_pattern table with lesson_ID
        # db.session.add(lesson)
        # db.session.commit()
        flash('Lesson added!')
        
        # return redirect(url_for('main.index'))

    else:
            print("not valid")

    return render_template(
                            'add_lesson.html',
                            title='Add Lesson',
                            form=form)


@bp.route('/add_student/<id>', methods=['GET', 'POST'])
@login_required
# pass account id in link - use to add student
def add_student(id):
    form = AddStudentForm()
    h1 = 'Add A Student'
    account = Accounts.query.get(id)
    # if for validates
    if form.validate_on_submit():

        teacher = form.teacher_ID.data
        instrument = form.instrument.data
        # add formatting so names are capitalized
        student = Students(

            account_ID=id,
            teacher_ID=teacher.id,
            first_name=form.first_name.data.capitalize(),
            last_name=form.last_name.data.capitalize(),
            instrument=instrument.instrument,
            notes=form.notes.data
        )
        db.session.add(student)
        db.session.commit()
        flash('Student added!')

        return redirect(url_for('main.view_account', id=id))

    else:
            print("not valid")

    return render_template(
                            'add_student.html',
                            title='Add Student',
                            account=account,
                            h1=h1,
                            form=form)


@bp.route('/delete_account/<id>', methods=['GET', 'POST'])
@login_required
def delete_account(id):
    # figure out how to cascade attendance too
    account = Accounts.query.filter_by(id=id).first_or_404()

    attendance = Attendance. \
        query.filter_by(account_ID=id).all()

    if attendance:
        for attended in attendance:
            db.session.delete(attended)

    db.session.delete(account)
    db.session.commit()

    flash('Account Deleted')
    return redirect(url_for('main.index'))

    return render_template(
                            'delete_account.html',
                            account=account,
                            title='Delete')


@bp.route('/delete_student/<id>', methods=['GET', 'POST'])
@login_required
def delete_student(id):
    # figure out how to cascade attendance too
    student = Students.query.filter_by(id=id).first_or_404()

    attendance = Attendance. \
        query.filter_by(student_ID=id).all()

    if attendance:
        for attended in attendance:
            db.session.delete(attended)

    db.session.delete(student)
    db.session.commit()

    flash('Student Deleted')
    return redirect(url_for('main.index'))

    return render_template(
                            'delete_student.html',
                            student=student,
                            title='Delete')


@bp.route('/delete_teacher/<id>', methods=['GET', 'POST'])
@login_required
def delete_teacher(id):
    # figure out how to cascade attendance too
    teacher = Teachers.query.filter_by(id=id).first_or_404()

    db.session.delete(teacher)
    db.session.commit()
    # remind me
    flash('Teacher FIRED')
    return redirect(url_for('main.index'))

    return render_template(
                            'delete_teacher.html',
                            teacher=teacher,
                            title='Delete')


@bp.route('/edit_account/<id>', methods=['GET', 'POST'])
@login_required
def edit_account(id):
    account = Accounts.query.filter_by(id=id).first_or_404()
    h1 = 'Edit Account'
    edit = True
    form = AddAccountForm(account.primary_email, account.secondary_email, edit)
    if form.validate_on_submit():

        # do not allow phone numbers to be blank
        if (form.primary_cell_phone.data == ""
                and form.primary_home_phone.data == ""
                and form.secondary_cell_phone.data == ""
                and form.secondary_home_phone.data == ""):
            # wish I knew how to repopulate the form

            flash('Please enter a phone number')
            return redirect(url_for('main.edit_account', id=id))

        account.primary_fname = form.primary_fname.data.capitalize()
        account.primary_lname = form.primary_lname.data.capitalize()
        account.primary_cell_phone = form.primary_cell_phone.data
        account.primary_email = form.primary_email.data
        account.primary_home_phone = form.primary_home_phone.data
        account.secondary_fname = form.secondary_fname.data.capitalize()
        account.secondary_lname = form.secondary_lname.data.capitalize()
        account.secondary_cell_phone = form.secondary_cell_phone.data
        account.secondary_email = form.secondary_email.data
        account.secondary_home_phone = form.secondary_home_phone.data

        db.session.commit()

        flash('Your changes have been saved.')
        return redirect(url_for('main.view_account', id=id))

    elif request.method == 'GET':
        form.primary_fname.data = account.primary_fname
        form.primary_lname.data = account.primary_lname
        form.primary_cell_phone.data = account.primary_cell_phone
        form.primary_email.data = account.primary_email
        form.primary_home_phone.data = account.primary_home_phone
        form.secondary_fname.data = account.secondary_fname
        form.secondary_lname.data = account.secondary_lname
        form.secondary_cell_phone.data = account.secondary_cell_phone
        form.secondary_email.data = account.secondary_email
        form.secondary_home_phone.data = account.secondary_home_phone

    return render_template(
                            'edit_account.html',
                            title='Edit Account',
                            form=form,
                            h1=h1,
                            account=account)


@bp.route('/edit_student/<id>', methods=['GET', 'POST'])
@login_required
def edit_student(id):
    student = Students.query.filter_by(id=id).first_or_404()
    form = AddStudentForm()
    h1 = 'Edit Student'
    if form.validate_on_submit():

        teacher = form.teacher_ID.data
        instrument = form.instrument.data

        student.teacher_ID = teacher.id
        student.first_name = form.first_name.data.capitalize()
        student.last_name = form.last_name.data.capitalize()
        student.instrument = instrument.instrument
        student.notes = form.notes.data
        db.session.commit()

        flash('Your changes have been saved.')
        return redirect(url_for('main.view_student', id=id))

    elif request.method == 'GET':

        form.first_name.data = student.first_name
        form.last_name.data = student.last_name
        form.notes.data = student.notes

    return render_template(
                            'edit_student.html',
                            title='Edit Student',
                            form=form,
                            h1=h1,
                            student=student)


@bp.route('/edit_teacher/<id>', methods=['GET', 'POST'])
@login_required
def edit_teacher(id):
    teacher = Teachers.query.filter_by(id=id).first_or_404()
    form = EditTeacherForm(teacher.email, teacher.username, teacher.phone_num)
    if form.validate_on_submit():

        teacher.first_name = form.first_name.data.capitalize()
        teacher.last_name = form.last_name.data.capitalize()
        teacher.phone_num = form.phone_num.data
        teacher.email = form.email.data
        teacher.address = form.address.data
        teacher.city = form.city.data.capitalize()
        teacher.state = form.state.data
        teacher.zipcode = form.zipcode.data
        teacher.is_admin = form.is_admin.data
        teacher.notes = form.notes.data
        teacher.username = form.username.data

        db.session.commit()
        print('valid')
        flash('Your changes have been saved.')
        return redirect(url_for('main.view_all_teachers'))

    elif request.method == 'GET':
        print('here')
        form.first_name.data = teacher.first_name
        form.last_name.data = teacher.last_name
        form.email.data = teacher.email
        form.address.data = teacher.address
        form.city.data = teacher.city
        form.state.data = teacher.state
        form.zipcode.data = teacher.zipcode
        form.is_admin.data = teacher.is_admin
        form.notes.data = teacher.notes
        form.username.data = teacher.username

    print('not valid')
    return render_template(
                            'edit_teacher.html',
                            form=form,
                            teacher=teacher,
                            title='Edit')


@bp.route('/view_account/<id>', methods=['GET', 'POST'])
@login_required
def view_account(id):
    account = Accounts.query.filter_by(id=id).first_or_404()

    return render_template(
                            'view_account.html',
                            title='Account',
                            account=account)


@bp.route('/view_all_teachers', methods=['GET', 'POST'])
@login_required
def view_all_teachers():
    teachers = Teachers.query.all()

    return render_template(
                            'view_all_teachers.html',
                            title='Teachers',
                            teachers=teachers)


@bp.route('/view_student/<id>', methods=['GET', 'POST'])
@login_required
def view_student(id):
    # not checked in default
    checked_in = False
    # get student id
    student = Students.query.filter_by(id=id).first_or_404()
    # get account id
    account_ID = student.account_ID
    # get today's date. maybe delete this line
    today = strftime('%Y-%m-%d')  # 2018-10-19
    # key word arguments for query
    kwargs = {'student_ID': id, 'account_ID': account_ID}
    # query attendance table with kwargs
    attendance = Attendance. \
        query.filter_by(**kwargs).order_by(Attendance.id.desc()).first()
    # convert time zone from UTC to local time
    from_zone = tz.tzutc()
    to_zone = tz.tzlocal()
    # get today's date
    utc = g.today.replace(tzinfo=from_zone)
    # convert time zone to local time zone
    today_my_time = utc.astimezone(to_zone)
    # check to see if student was checked in today
    if attendance is not None:
        # set dates student was present to var 'utc'
        utc = attendance.was_present
        # tell datetime object the timezone is utc since object is naive
        utc = utc.replace(tzinfo=from_zone)
        # convert time zone to local time zone
        my_time_zone = utc.astimezone(to_zone)
        # check to see if student was checked in today
        if (today_my_time.strftime('%Y-%m-%d')
                == my_time_zone.strftime('%Y-%m-%d')):
            # set check_in = true, so template won't display check in option
            print(my_time_zone)
            checked_in = True

    check_in_form = AttendanceForm()
    undo_check_in_form = AttendanceForm()

    if check_in_form.validate_on_submit() and checked_in is False:
        # if not yet checked in template displays this version of the form
        # adds a timestamp to db, checking student in
        was_present = Attendance(

                student_ID=student.id,
                account_ID=student.account_ID
            )

        db.session.add(was_present)
        db.session.commit()

        return redirect(url_for('main.view_student', id=id))

    # if student is checked in, template dispays this version of the form
    if undo_check_in_form.validate_on_submit() and checked_in is True:
        # deletes the last record for that student in attendance table
        delete_record = Attendance. \
            query.filter_by(**kwargs).order_by(Attendance.id.desc()).first()

        # undoes the check in for today's date
        db.session.delete(delete_record)
        db.session.commit()
        return redirect(url_for('main.view_student', id=id))

    return render_template(
                            'view_student.html',
                            title='Student',
                            check_in_form=check_in_form,
                            undo_check_in_form=undo_check_in_form,
                            checked_in=checked_in,
                            attendance=attendance,
                            today=today,
                            student=student)


@bp.route('/view_teacher/<id>', methods=['GET', 'POST'])
@login_required
def view_teacher(id):
    teacher = Teachers.query.get(id)

    return render_template(
                        'view_teacher.html',
                        title='Teacher',
                        teacher=teacher)
