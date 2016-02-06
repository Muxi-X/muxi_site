# coding: utf-8

"""
    likes.py
    ~~~~~~~~

        返回点赞数的API
"""

from . import api
from muxiwebsite.models import Blog
from flask import jsonify
from muxiwebsite import db


@api.route('/blog/<int:id>/likes/')
def blog_id_likes(id):
    """返回特定id博客"""
    blog = Blog.query.get_or_404(id)
    return jsonify({
        "%d" % id: blog.likes_number
    }), 200


@api.route('/blog/<int:id>/likes/', methods=['GET', 'POST'])
def like_id_blog(id):
    blog = Blog.query.get_or_404(id)
    blog.likes_number += 1
    db.session.add(blog)
    db.session.commit()
    return jsonify({
        "%d" % id: blog.likes_number
    }), 201

