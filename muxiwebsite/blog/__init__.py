# coding: utf-8

from flask import Blueprint


blogs = Blueprint(
    'blogs',
    '__name__',
    static_folder='static',
    template_folder='template'
)


from . import forms, views
