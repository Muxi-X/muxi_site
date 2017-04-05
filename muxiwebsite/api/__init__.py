# coding: utf-8

from flask import Blueprint

api = Blueprint(
    'api',
    __name__,
    subdomain = 'api',
)

from . import authentication, users,  comments,  shares,  users,  find, \
              likes,  signup,  login,  profile
