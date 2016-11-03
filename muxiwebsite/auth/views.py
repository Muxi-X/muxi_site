# coding: utf-8

"""
    views.py
    ~~~~~~~~

        视图文件
        /login: 统一登录页
        /logout: 统一登出页
"""

from . import auth
from .. import db
from ..models import User
from .forms import LoginForm, RegisterForm
from flask import render_template, redirect, request, url_for, flash, session
from flask.ext.login import login_user, login_required, logout_user, current_user
import base64
import sys


reload(sys)
sys.setdefaultencoding('utf-8')


@auth.route('/login/', methods=["POST"])
def login1():
    """登录页面"""
    form = LoginForm()
    user = User.query.filter_by(username=form.username.data).first()
    if user is not None and user.verify_password(form.password.data):
        login_user(user)
        if session['refer'] and not session['refer'].endswith(url_for("auth.register")):
            return redirect(session['refer'])
        else:
            return redirect(url_for('profile.user_profile', id=current_user.id))
    else:
        flash("用户名或密码不存在!")
        return redirect(url_for("auth.login"))


@auth.route('/login/', methods=["GET"])
def login():
    if not request.referrer == url_for('auth.login', _external=True):
        session['refer'] = request.referrer
    form = LoginForm()
    if form.validate_on_submit():
        return redirect(url_for('auth.login1'))
    return render_template("muxi_login.html", form=form)


@auth.route('/register/', methods=["POST", "GET"])
def register():
    """注册页面"""
    form = RegisterForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None:
            flash("username has been registered!")
            return redirect(url_for("auth.register"))
        elif form.password.data != form.passwordconfirm.data:
            flash("password do not match!")
            return redirect(url_for("auth.register"))
        else:
            user = User(
                    username=form.username.data,
                    email=form.email.data,
                    password=base64.b64encode(form.password.data),
                    avatar_url='http://7xrvvt.com1.z0.glb.clouddn.com/shakedog.gif',
                    role_id=3
                    )
            db.session.add(user)
            db.session.commit()
            return redirect(url_for("auth.login"))
    return render_template("muxi_register.html", form=form)


@login_required
@auth.route('/logout/')
def logout():
    """登出界面"""
    logout_user()
    return redirect(url_for('index'))
