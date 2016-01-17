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
from ..redirect_urls import is_safe_url, get_redirect_target, redirect_back


@auth.route('/login/', methods=["POST", "GET"])
def login():
    """登录页面"""
    next = get_redirect_target()
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None and user.verify_password:
            login_user(user)
            return redirect_back('profile.user_profile', id=current_user.id)
        flash("用户名或密码不存在!")
    return render_template("muxi_login.html", form=form, next=next)


@login_required
@auth.route('/logout/')
def logout():
    """登出界面"""
    logout_user()
    return redirect(url_for('shares.index', page = 1))

