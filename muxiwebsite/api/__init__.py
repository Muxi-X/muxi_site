# coding: utf-8

from flask import Blueprint

api = Blueprint(
    'api',
    __name__,
    subdomain='api',
    template_folder = 'templates',
    static_folder = 'static'
)


from . import authentication, users, comments, shares, users, find, \

        likes, signup, login, profile, blog
