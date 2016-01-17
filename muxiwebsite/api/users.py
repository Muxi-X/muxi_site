# coding: utf-8

"""
    users.py
    ========

    木犀官网用户API文档

"""
from flask import request, url_for, jsonify, current_app
from . import api
from muxiwebsite.models import User
from muxiwebsite import db


@api.route('/users/', methods=['GET'])
def get_users():
    """
    获取全部用户信息
    """
    page = request.args.get('page', 1, type=int)
    pagination = User.query.paginate(
        page,
        per_page=current_app.config['MUXI_USERS_PER_PAGE'],
        error_out=False
    )
    users = pagination.items
    prev = None
    if pagination.has_prev:
        prev = url_for('api.get_users', page=page-1, _external=True)
    next = None
    if pagination.has_next:
        next = url_for('api.get_users', page=page+1, _external=True)
    users_count = len(User.query.all())
    page_count = users_count//current_app.config['MUXI_USERS_PER_PAGE']
    if not isinstance(page_count, int) \
            or page_count == 0:
        page_count = page_count + 1
    last = url_for('api.get_users', page=page_count, _external=True)
    return jsonify({
        'users': [user.to_json() for user in users],
        'count': pagination.total
    }), 200, {'link': '<%s>; rel="next", <%s>; rel="last"' % (next, last)}


@api.route('/users/', methods=['POST', 'GET'])
def new_user():
    """
    注册一个用户
    """
    user = User(
        username = request.args.get('username'),
        password = request.args.get('password'),
        email = request.args.get('email')
    )
    db.session.add(user)
    db.session.commit()
    return jsonify({
        'new user' : user.id
    }), 201


@api.route('/users/<int:id>/shares/', methods=['GET'])
def get_users_id_shares(id):
    """
    获取特定id用户的所有分享
    """
    user = User.query.get_or_404(id)
    comments = user.share
    return jsonify({
        'comments' : [comment.to_json2() for comment in comments]
    }), 200

