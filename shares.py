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

tags = ['frontend', 'backend', 'android', 'design', 'product']

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


# 展示特定id的分享,相关评论,发表评论
@api.route('/views/<int:id>',methods=["GET"."POST"])
def view_share(id) :
    share = Share.query.get_or_404(id)
    share.author =
    User.query.filter_by(id=share.author_id).fisrt().username
    comments = Comment.query.filter_by(share_id=share.id).all()
    
    if request.method == 'POST' :
        comment = Comment()
        comment.comment = request.get_json().get("comment")
        comment.share_id = id 
        comment.author_id = current_user.id 
        comment.count = 0 
        comment.auhtor_name =
        User.query.filter_by(id=current_user.id).first().username

        db.session.add(comment)
        db.session.commit()
        this_comment = Comment.query.filter_by(
            comment = comment.comment.data ,    
            author_id = current_user.id,
            share_id = id ,
                ).first() 
        this_comment.count += 1 
        return jsonify(comment.to_json()) , 201 
    
    share_avatar =
    User.query.filter_by(id=share.author_id).first().avator_url
    share_comments_num =




@login_required
@api.route('/send/',methods=['GET','POST'])
    def add_share() :
        if request.method == 'POST' :
            share = Share() 
            share.title =  request.get_json.get("title")
            share.share = request.get_json.get("share")
            share.tag = request.get_json.get("tag")
            share.content = request.get_json.get("content")
            share.author_id = current_user.id
            db.session.add(share)
            db.session.commit()
            return redirect(url_for('.index',page))
        return jsonify(share.to_json2()) ,201 


@login_required
@api.route('/delete/<int:id>',methods=['GET','DELETE'])
@permission_required(Permission.WRITE_APTICLES)
def delete(id) :
    share = Share.query.get_or_404(id)
    if request.method == 'DELETE' :
        db.session.delete(share)
        db.session.commit()
        return jsonify({
            'deleted' : share.id 

            }) , 200 



@api.route('/edit-share/<int:id>/', methods=["PUT", "GET"])
@login_required
@permission_required(Permission.WRITE_ARTICLES)
def edit(id) :
    share = Share.query.get_or_404(id) 
    if request.method == 'put' :
        share.share = request.get_json().get("share")
        share.title = request.get_json().get("title")
        db.session.add(share)
        db.session.commit()
        return jsonify({
            'edited' : share.id  
            }) , 200 


@api.route('/')
def index() :

