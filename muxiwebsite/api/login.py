# coding: utf-8

"""
    login.py
    ~~~~~~~~

    木犀官网登陆API

"""

from flask import jsonify, request
from . import api
from muxiwebsite.models import User
from muxiwebsite import db

@api.route('/login/', methods=['POST'])
def login():
    email = request.get_json().get("email")
    pwd = request.get_json().get("password")

    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({}), 400
    if not user.verify_password(pwd):
        return jsonify({}), 400

    token = user.generate_auth_token()
    return jsonify ({
        'token': token
        }), 200
