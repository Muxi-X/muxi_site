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
from .forms import LoginForm
from flask import render_template, redirect, request, url_for, flash
from flask.ext.login import login_user, login_required, logout_user, current_user


@auth.route('/login', methods=["POST", "GET"])
def login():
    """登录页面"""
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None and user.verify_password:
            login_user(user)
            # use next to redirect
            return redirect(url_for('shares.index', page = 1))
        flash("用户名或密码不存在")
    return render_template("muxi_login.html", form=form)


@login_required
@auth.route('/logout')
def logout():
    """登出界面"""
    logout_user()
    return redirect(url_for('shares.index', page = 1))

