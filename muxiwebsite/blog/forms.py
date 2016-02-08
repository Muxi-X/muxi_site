# coding: utf-8
"""
    forms.py
    ~~~~~~~~

        博客表单
"""

from flask_wtf import Form
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import Required


class CommentForm(Form):
    """
    评论表单
    """
    comments = TextAreaField(validators=[Required()])
    submit = SubmitField()
