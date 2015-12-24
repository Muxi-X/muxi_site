# coding: utf-8
from . import profile
from flask import render_template


# test views
@profile.route('/test/')
def test():
    return "<h1>just tell you everything is ok!</h1>"

