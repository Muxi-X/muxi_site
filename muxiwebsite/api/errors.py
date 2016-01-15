# coding: utf-8

"""
    error.py
    ~~~~~~~

    错误处理程序

"""

from flask import jsonify
from . import api


# 404
def not_found(message):
    response = jsonify({'error': 'not_found', 'message': message})
    response.status_code = 404
    return response


# 404
def bad_request(message):
    response = jsonify({'error': 'bad_request', 'message': message})
    response.status_code = 400
    return response


# 401
def unauthorized(message):
    response = jsonify({'error': 'unathorized', 'message': message})
    response.status_code = 401
    return response


# 403
def forbidden(message):
    response = jsonify({'error': 'forbidden', 'message': message})
    response.status_code = 403
    return response


# 500
def server_error(message):
    response = jsonify({'error': 'server_error', 'message': message})
    response.status_code = 500
    return response

