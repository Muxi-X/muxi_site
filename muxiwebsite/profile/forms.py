# coding: utf-8
from flask_wtf import Form
from wtforms import StringField, SubmitField, TextAreaField, BooleanField,SelectField
from wtforms.validators import Required


class EditForm(Form):
    """
    用户个人信息编辑表单
    """
    username = StringField('username', validators=[Required()])
    avatar_url = StringField('avatar_url', validators=[Required()])
    info =  TextAreaField('info', validators=[Required()])

    email = StringField('email')
    birthday = StringField('birthday')
    hometown = StringField('hometown')
    group = SelectField('group',choices=[('backend','后台'),('frontend','前端'),('android','android'),('product','产品'),('design','设计')])
    timejoin = StringField('timejoin')
    timeleft = StringField('timeleft')
    left = BooleanField('left')

    personal_blog = StringField('personal_blog')
    github = StringField('github')
    flickr = StringField('flickr')
    weibo = StringField('weibo')
    zhihu = StringField('zhihu')

