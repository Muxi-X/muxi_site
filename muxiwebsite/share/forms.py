# coding: utf-8

"""
    forms.py
    ~~~~~~~~

        muxishare表单文件
"""

from flask.ext.wtf import Form
from wtforms.fields import StringField, SubmitField, TextAreaField
from wtforms.validators import Required
from flask.ext.pagedown.fields import PageDownField


class ShareForm(Form):
    """分享表单 markdown编辑器"""
    title = StringField(validators=[Required()])
    share = PageDownField(validators=[Required()])
    submit = SubmitField('分享')


class CommentForm(Form):
    """评论表单, 一般的表单"""
    comment = TextAreaField(validators=[Required()])
    submit = SubmitField('评论')


class EditForm(Form):
	"""编辑表单"""
	title = StringField(validators=[Required()])
	share = PageDownField(validators=[Required()])
	submit = SubmitField('修改')

