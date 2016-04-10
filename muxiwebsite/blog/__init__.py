# coding: utf-8

from flask import Blueprint


blogs = Blueprint(
    'blogs',
    __name__,
    subdomain='blog',
    template_folder='templates',
    static_folder='static',
)


from . import forms, views
