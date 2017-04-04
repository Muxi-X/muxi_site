# coding: utf-8

"""
    share.py
    ~~~~~~~~

    木犀分享的信息

"""

from flask import url_for, jsonify, request, g, current_app
from muxiwebsite.models import Share, AnonymousUser , User , Comment 
from muxiwebsite import db
from .authentication import auth
from flask_login import current_user 
from ..decorators import permission_required 
from . import api

tags = ['frontend', 'backend', 'android', 'design', 'product']

@api.route('/shares/all/', methods=['GET'])
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
    per_page = current_app.config['MUXI_SHARES_PER_PAGE']
    pages_count = pagination.total / per_page + 1
    if page > pages_count :
        return jsonify({}),  404 
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
    author_name = []

    return jsonify({
        'shares': [ share.to_json()  for share in shares ],
        'count': pagination.total , 
        'page' : page , # 当前页数
        'pages_count' : pages_count , 
    }), 200, {'link': '<%s>; rel="next", <%s>; rel="last"' % (next, last)}


@api.route('/shares/<int:id>/comments/',methods=["GET"])
def view_share(id) :
    '''
    查看某一篇分享的评论
    '''
    share = Share.query.get_or_404(id) 
    comments = Comment.query.filter_by(share_id=id).all()

    return jsonify({
         [ comment.to_json() for comment in comments ] ,
        }) ,200  

@api.route('/shares/<int:id>/add_comment/',methods=['POST']) 
def add_comment(id) :
    ''' 
    登录用户发表评论
    '''
    token = request.headers.get("token") 
    try :
        current_user_id = User.verify_auth_token(token).id
    except AttributeError :
        return jsonify({
            'message':'You can not send a comment '
            }),400 

    comment = Comment()
    comment.comment = request.get_json().get("comment")
    comment.share_id = id 
    comment.author_id = current_user_id 

    db.session.add(comment)
    db.session.commit()

    return jsonify({
        'message' : 'You add a comment successfully!'
        }) , 200 


@api.route('/shares/send/',methods=['POST'])
def add_share() :
    '''
    登录用户发送分享
    '''
    token = request.headers.get("token")
    try :
        current_user_id = User.verify_auth_token(token).id
    except AttributeError :
        return jsonify({
            'message' : 'You can not send a share'
            }) , 404 

    share = Share()       
    share.title =  request.get_json().get("title")
    share.share = request.get_json().get("share") 
    share.tag = request.get_json().get("tags")    
    share.author_id = current_user_id

    db.session.add(share)
    db.session.commit()

    return jsonify( { 
                    "share" : share.share ,
                    "title" : share.title ,    
                    "tag" : share.tag ,    
                    "author_id" : share.author_id ,
                    "id" :  share.id , 
                    } ) , 200 

@api.route('/shares/<int:id>/delete/',methods=['DELETE'])
def delete(id) :
    '''
    删除分享(发送分享的用户)
    '''
    share = Share.query.get_or_404(id)
    token = request.headers.get("token")
    try :
        current_user_id = User.verify_auth_token(token).id
    except AttributeError :
        return jsonify({
            'message': 'login first'
            }) , 404 

    author_id = Share.query.filter_by(id=id).first().author_id
    if  current_user_id != author_id :
        return jsonify({
            'message' : 'you can not delete it!'
            }) , 404 

    db.session.delete(share)
    db.session.commit()
    return jsonify({
            'deleted' : share.id  , 
            }) , 200 
        
@api.route('/shares/<int:id>/views/',methods=['GET'])
def views(id) :
    '''
    查看单个分享,和它所有的评论
    '''
    share = Share.query.get_or_404(id)
    comments = Comment.query.filter_by(share_id=id).all()
    return jsonify ({
        'share' : share.to_json() ,
        'comments' : [ comment.to_json() for comment in comments ] ,
        }) ,200 


@api.route('/shares/<int:id>/edit/', methods=["PUT"])
def edit(id) :
    '''
    编辑已经发送的分享(发送该分享的用户)
    '''
    share = Share.query.get_or_404(id) 
    token = request.headers.get("token")
    try :
        current_user_id = User.verify_auth_token(token).id
    except AttributeError :
        return jsonify({
            'message' : 'login first! '
            }) , 400 

    author_id = Share.query.filter_by(id=id).first().author_id
    if  current_user_id != author_id :
        return jsonify({
            'message': 'You can not edit!'
            }) , 404

    share.share = request.get_json().get("share")
    share.title = request.get_json().get("title")

    db.session.add(share)
    db.session.commit()
    return jsonify({
            'edited' : share.id  ,
            }) , 200 


@api.route('/shares/',methods=['GET'])
def index() :
    '''
    分享首页,根据所选标签显示分享
    '''
    page = request.args.get('page',1,type=int) 
    sort_args = request.args.get("sort")
    if sort_args == None :
        shares_pages = \
        Share.query.order_by('-id').paginate(page,current_app.config['SHARE_PER_PAGE'],False)
        pages_count = shares_pages.total / current_app.config['SHARE_PER_PAGE'] + 1 
        if page > pages_count : 
            return jsonify({
                'message' : 'can not find the page!'
                }) , 404 
        shares = shares_pages.items 

    elif sort_args == "hot" :
        shares_count = {}
        shares = []
        for share in Share.query.all():
            shares_count[share] = share.comment.count()
        shares_count = sorted(shares_count.items(), lambda x ,y : cmp(y[1],x[1]))
        for tuple_ in shares_count :
            shares.append(tuple_[0])
        shares = shares[:5]
        pages_count = 1 
        shares_pages = None

    elif sort_args in tags :
        shares = []
        item = Share.query.filter_by(tag=sort_args)
        shares_pages = item.order_by('-id').paginate(page,current_app.config['SHARE_PER_PAGE'],False)
        pages_count = shares_pages.total / current_app.config['SHARE_PER_PAGE'] + 1
        shares = shares_pages.items 
        if page > pages_count : 
            return jsonify({
                'message' : 'can not find the page!'
                }) , 404

    return jsonify({
            'pages_count' : pages_count ,
            'page' : page , 
            'share' : [share.to_json() for share in shares ] , 
     }) , 200 
    
