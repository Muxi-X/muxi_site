# coding: utf-8

"""
    forms.py
    ~~~~~~~~

        表单文件
"""

from flask_wtf import Form
from wtforms.fields import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import Required


class LoginForm(Form):
    """登录表单"""
    username = StringField('用户名', validators=[Required()])
    password = PasswordField('密码', validators=[Required()])
    remember_me = BooleanField('记住我')
    submit = SubmitField('登录')


class RegisterForm(Form):
    """注册表单"""
    username = StringField('用户名', validators=[Required()])
    email = StringField('邮箱', validators=[Required()])
    password = PasswordField('密码', validators=[Required()])
    passwordconfirm = PasswordField('确认密码', validators=[Required()])
    submit = SubmitField('注册')
