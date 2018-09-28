from flask import render_template, flash, redirect, url_for, request, g, \
    jsonify, current_app
from flask_login import current_user, login_required
from app import db
from app.models import Teachers
from app.main import bp
from pprint import pprint, PrettyPrinter

@bp.route('/')
@bp.route('/index')
@login_required
def index():

    teacher = Teachers.query.all()
    #pp = pprint.PrettyPrinter(teacher)
    print('FECKKK')
    pprint(teacher)
    print('FARRRRRKKKKK')
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
    return render_template('index.html', title='Home', user=user, posts=posts, teacher=teacher)