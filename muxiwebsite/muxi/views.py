# coding: utf-8

"""
    muxi/views.py:

        木犀官网的视图函数
"""

from flask import render_template
from . import muxi

def is_mobie():
    platform = request.user_agent.platform
    if platform in ["android", "iphone", "ipad"]:
        return True
    else:
        return False

@muxi.route('/')
def muxi_index():
		flag = is_mobie()
    if flag:
        return render_template("index_m.html")
    else:
				return render_template('index_d.html')

@muxi.route('/join')
def muxi_index():
		flag = is_mobie()
    if flag:
        return render_template("join.html")
    else:
				return render_template('join.html')

