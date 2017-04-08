<<<<<<< HEAD
# coding: utf-8
=======
# -*- coding: utf-8 -*-
>>>>>>> a6580b6da6d98229503940f7f81006bce384c9d4

"""
    signup.py
    ~~~~~~~~~
    木犀官网注册API
"""

from flask import jsonify, g, request
from . import api
<<<<<<< HEAD
from flask import jsonify , g , request
=======
>>>>>>> a6580b6da6d98229503940f7f81006bce384c9d4
from muxiwebsite.models import User
from .authentication import auth
from muxiwebsite import db
from werkzeug.security import generate_password_hash
import base64

@api.route('/signup/', methods=['POST'])
def signup():
    """用户注册"""
    un = request.get_json().get("username")
    email = request.get_json().get("email")
    password = request.get_json().get("password")

    if User.query.filter_by(username=un).first() is not None:
        return jsonify ({}), 400
    if User.query.filter_by(email=email).first() is not None:
        return jsonify ({}), 400
    if un is None or email is None or password is None:
        return jsonify ({}), 400

    user = User(
<<<<<<< HEAD
            username = un ,
            email = email ,
            password = password
            )
=======
        username = un,
        email = email,
        password = base64.b64encode(password),
        avatar_url = "http://7xrvvt.com1.z0.glb.clouddn.com/shakedog.gif",
        role_id = 3
        )
>>>>>>> a6580b6da6d98229503940f7f81006bce384c9d4

    db.session.add(user)
    db.session.commit()

    return jsonify({
<<<<<<< HEAD
        'created' : user.id
        }) , 200
=======
        "created": user.id
        }), 200
>>>>>>> a6580b6da6d98229503940f7f81006bce384c9d4
