# coding: utf-8

"""
    comments.py
    ~~~~~~~~~~

    木犀官网评论API

"""

from flask import jsonify, g, request
from . import api
from muxiwebsite.models import Share
from muxiwebsite.models import Comment
from .authentication import auth
from muxiwebsite import db


@api.route('/shares/<int:id>/comments/')
def get_shares_id_comments(id):
    share = Share.query.get_or_404(id)
    comments = share.comment.all()
    return jsonify({
        'comments' : [comment.to_json() for comment in comments]
    }), 200


@api.route('/shares/<int:id>/comments/', methods=['GET', 'POST'])
@auth.login_required
def new_shares_id_comments(id):
    """向特定分享发评论"""
    data_dict = eval(request.data)
    share = Share.query.get_or_404(id)
    if not hasattr(g.current_user, 'id'):
        return jsonify({
            'error' : 'plase login first'
        }), 403
    comment = Comment(
        comment = data_dict.get('comment'),
        author_id = g.current_user.id,
        share_id = share.id
        # date = request.args.get('date')
    )
    db.session.add(comment)
    db.session.commit()
    return jsonify({
        'new comment' : comment.id
    }), 201

