# -*- coding: utf-8 -*-

"""
    signup.py
    ~~~~~~~~~

    木犀官网注册API

"""

from flask import jsonify, g, request
from . import api
from muxiwebsite.models import User
from .authentication import auth
from muxiwebsite import db

@api.route('/signup/', methods=['POST'])
def signup():
    """用户注册"""
 #   return "OK"
    un = request.get_json().get("username")
    email = request.get_json().get("email")
    password = request.get_json().get("password")

    if User.query.filter_by(username=un).first() is not None:
        return jsonify ({}), 400
    if User.query.filter_by(email=email).first() is not None:
        return jsonify ({}), 400
    if un is None or email is None or password is None:
        return jsonify ({}), 400

    user = User(username = un, email = email, password=password)
    db.session.add(user)
    db.session.commit()

    return jsonify({
        "created": user.id
        }), 200
