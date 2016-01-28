# coding: utf-8

"""
    filter.py
    ~~~~~~~~~

        自定义jinja装饰器

"""

from muxiwebsite import app
from muxiwebsite.share import share
from flask import Markup
import markdown


# markdown装饰器
# @app.template_filter('neomarkdown')
@share.template_filter('neomarkdown')
def neomarkdown(markdown_content):
    content = Markup(markdown.markdowm(markdown_content))
    return content
