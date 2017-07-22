#!/usr/bin/env python
# encoding: utf-8

from flask import jsonify, request
from muxiwebsite.models import User
from muxiwebsite import db

class Login() :
    def __init__(self,email,pwd) :
        self.email = email
        self.pwd = pwd

    def login(self):
        user = User.query.filter_by(email=self.email).first()
        token = " "
        if not user:
            return jsonify({}), 403
        if not user.verify_password(self.pwd):
            return jsonify({}), 400
        token = user.generate_auth_token()
        return   token , 200

