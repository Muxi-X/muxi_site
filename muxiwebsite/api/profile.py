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

    if not user or not user.verify_auth_token(token):
        return jsonify({}), 403

    books = user.book
    book_ids = []
    for book in books:
        books_ids.append(book.id)

    shares = user.share
    share_ids = []
    for share in shares:
        share_ids.append(share.id)

    blogs = user.blogs
    blog_ids = []
    for blog in blog_ids:
        blog_ids.append(blog.id)

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
        "zhihu": user.zhihu,
        "book_ids": book_ids,
        "share_ids": share_ids,
        "blog_ids": blog_ids
        }), 200


    @api.route('/edit_profile/', methods=['POST'])
def edit_profile():
    """编辑用户信息"""
    token = request.headers.get('token') 
    un = request.args.get('username')

    user = User.query.filter_by(username=un).first()

    if not user or not user.id==User.verify_auth_token(token):
        return jsonify({}), 403

    user.avatar_url = request.get_json().get("avatar_url")
    user.birthday = request.get_json().get("birthday")
    user.flickr = request.get_json().get("flickr")
    user.github = request.get_json().get("github")
    user.group = request.get_json().get("group")
    user.hometown = request.get_json().get("hometown")
    user.info = request.get_json().get("info")
    user.personal_blog = request.get_json().get("personal_blog")
    user.timejoin = request.get_json().get("timejoin")
    user.timeleft = request.get_json().get("timeleft")
    user.weibo = request.get_json().get("weibo")
    user.zhihu = request.get_json().get("zhihu")

    db.session.add(user)
    db.session.commit()

    return jsonify({}) , 201
