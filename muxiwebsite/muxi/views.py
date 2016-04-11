# coding: utf-8

"""
    muxi/views.py:

        木犀官网的视图函数
"""

from flask import render_template
from . import muxi

@muxi.route('/')
def muxi_index():
    return render_template('index_d.html')

