# coding: utf-8

"""
    profile.py
    ~~~~~~~~~~

    木犀官网资料API

"""

from flask import jsonify, request
from . import api
from muxiwebsite.models import User
from muxiwebsite import db
import datetime

@api.route('/show_profile/', methods=['GET'])
def show_profile():
    """读取用户信息"""
    un = request.args.get('username')
    token = request.headers.get('token')

    user = User.query.filter_by(username=un).first()
    timejoin = datetime.date.today().strftime('%Y%m%d')
    timeleft = datetime.date.today().strftime('%Y%m%d')

    if not user or not user.verify_auth_token(token):
        return jsonify({}), 403

    return jsonify({
        "id": user.id, 
        "email": user.email, 
        "birthday": user.birthday, 
        "hometown": user.hometown,
        "group": user.group, 
        "timejoin": user.timejoin,
        "timeleft": user.timeleft,
        "username": un,
        "info": user.info,
        "avatar_url": user.avatar_url,
        "personal_blog": user.personal_blog,
        "github": user.github,
        "flickr": user.flickr,
        "weibo": user.weibo,
        "zhihu": user.zhihu
        })
