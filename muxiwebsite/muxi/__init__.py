# coding: utf-8

"""
    木犀官网静态页面

"""

from flask import Blueprint


muxi = Blueprint(
    'muxi',
    __name__,
    template_folder = 'templates',
    static_folder = 'static'
)

from . import views
