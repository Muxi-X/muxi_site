# coding: utf-8

"""
    muxi_site ~ Book

        木犀官网 木犀图书 部分

        木犀图书是木犀团队内部的图书借阅管理系统，方便木犀的小伙伴们借阅和管理书籍

        site: http://lib.muxistudio.com
        code: flask + html + css + js
"""

from flask import Blueprint


book = Blueprint(
    'book',
    __name__,
    template_folder = 'templates',
    static_folder = 'static'
)


from . import views, forms
