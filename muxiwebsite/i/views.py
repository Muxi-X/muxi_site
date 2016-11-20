# coding: utf-8

from . import i
from flask import render_template, redirect, url_for, request
from flask_login import login_required, current_user
from muxiwebsite.models import User


@login_required
@i.route('/')
def index():
    """
    木犀博客首页
    """
    return render_template("index.html", current_user=current_user)


@login_required
@i.route('/members/')
def members():
    """
    Show all members
    """
    users = User.query.all()

    # Group mambers' list initialization
    frontends = []
    backends = []
    androids = []
    designs = []
    products = []

    for user in users:
        if user.left == False:
            if user.group == 'frontend':
                frontends.append(user)
            elif user.group == 'backend':
                backends.append(user)
            elif user.group == 'android':
                androids.append(user)
            elif user.group == 'design':
                designs.append(user)
            elif user.group == 'product':
                products.append(user)

    return render_template(
            "members.html",
            frontends = frontends,
            backends = backends,
            androids = androids,
            designs = designs,
            products = products,
            current_user = current_user
            )
