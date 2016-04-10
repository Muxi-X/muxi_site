# coding: utf-8

"""
	views.py
	~~~~~~~~

		views for flask-admin
"""

from flask.ext.admin.contrib  import sqla
from flask.ext.admin import helpers, expose
from flask_admin import BaseView
import flask.ext.admin as admin
import flask.ext.login as login
from .auth.forms import LoginForm
from flask import redirect, url_for
from . import app


@app.route('/')
def index():
    return "index"
