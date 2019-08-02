from datetime import datetime
from flask import render_template, flash, redirect, url_for, request, g, \
    jsonify, current_app
from flask_login import current_user, login_required
from app import db
from app.models import User,UserData

from app.main import bp
from app.main.forms import AddUserForm, UpdateUserForm


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
                        name = form.name.data,title=form.title.data,status='normal')
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('添加成功')
        return redirect(url_for('main.index'))
    return render_template('main/add_user.html',title='添加用户',form=form)


@bp.route('/update_user', methods=['GET','POST'])
@login_required
def update_user():
    uid = request.args.get("uid")
    user = UserData.query.filter_by(id=uid).first()
    form = UpdateUserForm()

    if request.method == 'GET':
        if request.args.get("func") == 'update':
            form.username.data = user.username
            form.email.data = user.email
            form.name.data = user.name
            form.title.data = user.title
            form.status.data = user.status
            return render_template('main/update_user.html',title='修改用户',form=form)
        if request.args.get("func") == 'delete':
            user.status = 'deleted'         #逻辑删除：改状态位为0
            db.session.commit()
            flash('删除成功')
            return redirect(url_for('main.index'))

    if form.validate_on_submit():
        user.username = form.username.data
        user.email = form.email.data
        user.name = form.name.data
        user.title = form.title.data
        user.status = form.status.data
        db.session.commit()
        flash('修改成功')
        return redirect(url_for('main.index'))
    return redirect(url_for('main.index'))