# coding: utf-8

"""
    find.py
    ~~~~~~~

    查找用户名是否被占用

"""

from flask import request, jsonify
from . import api
from muxiwebsite.models import User


@api.route('/username/')
def find():
    """
    查找用户名是否被占用
    安卓提供用户名
    """
    username = request.args.get('username')
    register_username = []
    users = User.query.all()
    for user in users:
        register_username.append(user.username)
    if username in register_username:
        return jsonify({'username' : 1})
    else:
        return jsonify({'username' : 0})

