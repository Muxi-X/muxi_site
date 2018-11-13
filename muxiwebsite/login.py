#!/usr/bin/env python
# encoding: utf-8

from flask import jsonify, request ,current_app
from muxiwebsite.models import User
from muxiwebsite import db
import base64

class Login() :
    def __init__(self,username,pwd) :
        self.username = username
        self.pwd = pwd

    def login(self):
        user = User.query.filter_by(username=self.username).first()
        token = " "
        if not user:
            return jsonify({"msg":"no such user"}), 401
        if user.verify_password(self.pwd) :
            token = user.generate_auth_token()
            return token , 200
        try :
            pwd = base64.b64decode(self.pwd)
            pwd = unicode(pwd)
        except TypeError :
            return jsonify({"msg":"pwd decode error"}) , 401
        if not pwd == current_app.config["MUXI_SECRET_KEY"] :
            return jsonify({"msg":"wrong pwd"}), 401
        token = user.generate_auth_token()
        return  token , 200

