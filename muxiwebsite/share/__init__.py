# coding: utf-8

"""
    muxishare ~ 木犀团队的分享小站

        分享，是木犀的团队精神，这个小站类似于v2ex，不过分享者都是
        团队中的朋友，这会不一样 ~ ~ ~
"""

from flask import Blueprint

share = Blueprint(
    'share',
    __name__,
    template_folder = 'templates',
    static_folder = 'static'
)


from . import views, forms
"""@muxistudio bugday 2015年10月16日"""
