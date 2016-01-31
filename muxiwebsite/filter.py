# coding: utf-8

"""
    filter.py
    ~~~~~~~~~

        自定义jinja装饰器

"""

from muxiwebsite import app
from muxiwebsite.share import share
from flask import Markup
import markdown2


# markdown装饰器
@share.template_filter('neomarkdown')
def neomarkdown(markdown_content):
    content = Markup(markdown2.markdown(markdown_content, extras=["tables"]))
    return content
