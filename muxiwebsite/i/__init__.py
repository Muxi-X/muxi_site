# coding: utf-8

"""
    i.muxixyz.com

        内部官网

        site: http://lib.muxistudio.com
        code: flask + html + css + js
"""

from flask import Blueprint


i = Blueprint(
    'i',
    __name__,
    template_folder = 'templates',
    static_folder = 'static',
    subdomain = 'i'
)


from . import views
