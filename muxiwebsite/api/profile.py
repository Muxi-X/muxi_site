# coding: utf-8

"""
    profile.py
    ~~~~~~~~~~
    木犀官网资料API
"""

from flask import jsonify, request , g
from . import api
from muxiwebsite.models import User , Permission
from muxiwebsite import db
from .decorators import login_required , permission_required
import datetime

@api.route('/show_profile/', methods=['GET'])
@login_required
def show_profile():
    """读取用户信息"""
    ID = g.current_user.id
    user = User.query.filter_by(id=ID).first()

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
        "username": user.username,
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
@login_required
@permission_required(Permission.WRITE_ARTICLES)
def edit_profile():
    """编辑用户信息"""
    ID = g.current_user.id
    user = User.query.filter_by(id=ID).first()

    user.email = request.get_json().get("email")
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
