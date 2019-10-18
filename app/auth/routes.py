from flask import render_template, redirect, url_for, flash, request
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user
from app import db
from app.auth import bp
from app.auth.forms import LoginForm, TeacherRegistrationForm, \
	EditTeacherForm, UserRegistrationForm
from app.models import Teachers, User
# from app.auth.email import send_password_reset_email


@bp.route('/login', methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('main.index'))
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(username=form.username.data).first()
		if user is None or not user.check_password(form.password.data):
			flash('Invalid username or password')
			return redirect(url_for('auth.login'))
		login_user(user, remember=form.remember_me.data)
		next_page = request.args.get('next')
		if not next_page or url_parse(next_page).netloc != '':
			next_page = url_for('main.index')
		return redirect(next_page)
	return render_template('auth/login.html', title='Sign In', form=form)


@bp.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('main.index'))


# @bp.route('/register', methods=['GET', 'POST'])
# def register():
#     form = TeacherRegistrationForm()
#     if form.validate_on_submit():
#         user = Teachers(
#                     username=form.username.data,
#                     email=form.email.data,
#                     first_name=form.first_name.data.capitalize(),
#                     last_name=form.last_name.data.capitalize(),
#                     phone_num=form.phone_num.data,
#                     address=form.address.data,
#                     city=form.city.data.capitalize(),
#                     state=form.state.data,
#                     zipcode=form.zipcode.data,
#                     is_admin=form.is_admin.data,
#                     notes=form.notes.data
#                 )
#         user.set_password(form.password.data)
#         db.session.add(user)
#         db.session.commit()
#         flash('Teacher added.')
#         return redirect(url_for('main.index'))
#     return render_template('auth/register.html', title='Register',
#                            form=form)


@bp.route('/register', methods=['GET', 'POST'])
def register():
	form = UserRegistrationForm()
	if form.validate_on_submit():
		user = User(
			username=form.username.data,
		)
		user.set_password(form.password.data)
		db.session.add(user)
		db.session.commit()
		flash('User added.')
		return redirect(url_for('main.index'))
	return render_template('auth/register.html', title='Register',
						   form=form)
	