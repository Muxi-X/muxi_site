#!/usr/bin/env python
# encoding: utf-8

from  flask import jsonify, g, request
from muxiwebsite.models import User
from muxiwebsite import db
from werkzeug.security import generate_password_hash
import base64

class Signup() :
    def __init__(self,un,email,password) :
        self.un = un
        self.email = email
        self.password = password

    def signup(self):
        """用户注册"""

        ID = 0
        if User.query.filter_by(username=self.un).first() is not None:
            return jsonify ({}), 401
        if User.query.filter_by(email=self.email).first() is not None:
            return jsonify ({}), 402
        if self.un is None or self.email is None or self.password is None:
            return jsonify ({}), 403

        user = User(
            username = self.un,
            email = self.email,
            password = base64.b64encode(self.password),
            avatar_url = "http://7xrvvt.com1.z0.glb.clouddn.com/shakedog.gif",
            role_id = 3
            )

        db.session.add(user)
        db.session.commit()
        ID = user.id

        return  ID , 200
