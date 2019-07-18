from datetime import datetime
from flask import render_template, flash, redirect, url_for, request, g, \
    jsonify, current_app
from flask_login import current_user, login_required
from app import db
from app.models import User,UserData

from app.main import bp
from app.main.forms import AddUserForm


@bp.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    users = UserData.query.all()
    return render_template('index.html', title='主页',users=users)



@bp.route('/add_user',methods=['GET','POST'])
@login_required
def add_user():
    form = AddUserForm()
    if form.validate_on_submit():
        user = UserData(username= form.username.data,email= form.email.data,
                        name = form.name.data,title=form.title.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('添加成功')
        return redirect(url_for('main.index'))
    return render_template('main/add_user.html',title='添加用户',form=form)