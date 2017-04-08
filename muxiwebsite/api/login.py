<<<<<<< HEAD
# conding: utf-8
=======
# coding: utf-8

"""
    login.py
    ~~~~~~~~

    木犀官网登陆API

"""
>>>>>>> a6580b6da6d98229503940f7f81006bce384c9d4

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
        return jsonify({}), 403
    if not user.verify_password(pwd):
        return jsonify({}), 400

    token = user.generate_auth_token()
    return jsonify ({
<<<<<<< HEAD
            'token': token,
                }), 200
=======
        'token': token,
        }), 200
>>>>>>> a6580b6da6d98229503940f7f81006bce384c9d4

