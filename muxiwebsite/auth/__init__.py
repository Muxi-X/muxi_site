# coding: utf-8

"""
    muxi_site - auth:

        木犀官网统一个人页和统一登录页

        1. 权限系统
        2. 登录系统
        3. 个人主页 (位置待定)
"""

from flask import Blueprint


auth = Blueprint(
    'auth',
    __name__,
    subdomain = 'auth',
    template_folder = 'templates',
    static_folder = 'static'
)


from . import views, forms
"""@muxistudio bugday"""
