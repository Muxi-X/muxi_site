# coding: utf-8

"""
authentication.py
~~~~~~~~~~~~~~~~~
    API验证模块
    木犀官网API采用用户注册邮箱和token两种形式验证
    建议使用token，更加安全
"""

from flask import g, jsonify
from flask_httpauth import HTTPBasicAuth
from . import api
from ..models import User, AnonymousUser
from .errors import unauthorized, not_found, server_error


#  只需要在蓝图包中初始化
auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(username_or_token, password):
    """
    根据邮箱或token获取用户信息
    同密码进行比对验证
    """
    if username_or_token == '':
        g.current_user = AnonymousUser()
        return True

    if password == '':
        g.current_user = User.verify_auth_token(username_or_token)
        g.token_used = True
        return g.current_user is not None

    user = User.query.filter_by(username=username_or_token).first()
    if not user:
        return False

    g.current_user = user
    g.token_used = False

    return user.verify_password(password)


@api.before_request
def before_request():
    """
    保护API只允许登录用户访问
    并将错误处理递交 get_token 函数处理
    """
    pass


@api.route('/token/', methods=['POST', 'GET'])
@auth.login_required  # 只有登录用户可以请求token
def get_token():
    """
    获取token /api/v1.0/token
    :return:  token & time
    """
    if isinstance(g.current_user, AnonymousUser) or g.token_used:
        return unauthorized('Invalid credentials')
    return jsonify({
        'token': g.current_user.generate_auth_token(),
    })


@auth.error_handler
def auth_error():
    """
    验证错误处理
    :return:
    """
    return unauthorized('Invalid credentials')


@auth.error_handler
def not_found_error():
    """
    404错误处理
    :return:
    """
    return not_found('Not found')


@auth.error_handler
def server_error_error():
    """
    500错误处理
    :return:
    """
    return server_error('Server error')
