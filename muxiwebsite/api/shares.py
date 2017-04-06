# coding: utf-8

"""
    share.py
    ~~~~~~~~

    木犀分享的信息

"""

from flask import url_for, jsonify, request, g, current_app
from . import api
from muxiwebsite.models import Share, AnonymousUser
from muxiwebsite import db
from .authentication import auth
from flask_login import current_user

@api.route('/shares/', methods=['GET'])
def get_shares():
    """
    获取所有分享
    """
    page = request.args.get('page', 1, type=int)
    pagination = Share.query.paginate(
        page,
        per_page=current_app.config['MUXI_SHARES_PER_PAGE'],
        error_out=False
    )
    shares = pagination.items
    prev = None
    if pagination.has_prev:
        prev = url_for('api.get_shares', page=page-1, _external=True)
    next = None
    if pagination.has_next:
        next = url_for('api.get_shares', page=page+1, _external=True)
    shares_count = len(Share.query.all())
    page_count = shares_count//current_app.config['MUXI_SHARES_PER_PAGE']
    if not isinstance(page_count, int) \
            or page_count == 0:
        page_count = page_count + 1
    last = url_for('api.get_shares', page=page_count, _external=True)
    return jsonify({
        'shares': [share.to_json() for share in shares],
        'count': pagination.total
    }), 200, {'link': '<%s>; rel="next", <%s>; rel="last"' % (next, last)}


@api.route('/shares/', methods=['POST', 'GET'])
@auth.login_required
def new_share():
    """创建一个分享"""
    data_dict = eval(request.data)
    if not hasattr(g.current_user, 'id'):
        return jsonify({
            'error' : 'please login first'
        }), 403
    share = Share(
        title = data_dict.get('title'),
        share = data_dict.get('share'),
        author_id = g.current_user.id
    )
    db.session.add(share)
    db.session.commit()
    return jsonify({
        'new share' : share.id
    }), 201


