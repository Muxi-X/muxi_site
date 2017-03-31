# coding: utf-8

"""
    share.py
    ~~~~~~~~

    木犀分享的信息

"""

from flask import url_for, jsonify, request, g, current_app

from muxiwebsite.models import Share, AnonymousUser , User , Comment , Permission 
from muxiwebsite import db
from .authentication import auth
from flask_login import current_user 
from muxiwebsite.decorators import login_required 
from ..decorators import permission_required 
from . import api

tags = ['frontend', 'backend', 'android', 'design', 'product']

@api.route('/shares', methods=['GET'])
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
        'count': pagination.total , 
        'page' : page , # 当前页数
    }), 200, {'link': '<%s>; rel="next", <%s>; rel="last"' % (next, last)}


# 展示特定id的分享,相关评论,发表评论
@api.route('/views/<int:id>',methods=["GET","POST"])
def view_share(id) :
    share = Share.query.get_or_404(id) 
    share.author_id = Share.query.filter_by(id=id).first().author_id
    comments = Comment.query.filter_by(share_id=id).all()
    token = request.headers.get("token")
    try :
        current_user_id = User.verify_auth_token(token).id
    except :
        current_user_id = None 

    if request.method == 'POST' :
        if current_user_id is not None :
            comment = Comment()
            comment.comment = request.get_json().get("comment")
            comment.share_id = id 
            comment.author_id = current_user_id 

            db.session.add(comment)
            db.session.commit()
            return jsonify(comment.to_json()) , 201 
        return jsonify({ 
            
            'message' : 'you can not comment!' }),400 
    
        share.avatar = \
        User.query.filter_by(id=share.author_id).first().avator_url
    
    for comment in comments :
        comment.avatar = \
        User.query.filter_by(id=comment.author_id).first().avatar_url
        comment.username = \
        User.query.filter_by(id=comment.author_id).first().username
        comment.content  = comment.comment 

    return jsonify({
        "share" : share.share , 
        "title" : share.title ,
        "tag" : share.tag , 
        "author_id" : share.author_id ,
        "comments" : [comment.to_json() for comment in comments ] ,

        }) ,200 


@api.route('/send',methods=['POST'])
def add_share() :
    share = Share() 
    token = request.headers.get("token")
    share.title =  request.get_json().get("title")
    share.share = request.get_json().get("share")
    share.tag = request.get_json().get("tag")
    share.content = request.get_json().get("content")
    current_user = User.verify_auth_token(token)
    try :
        share.author_id = current_user.id
    except :
        return jsonify({
            
            'message' : 'you can not send a share!'
            }) , 200 
    db.session.add(share)
    db.session.commit()
    return jsonify( { 
                    "share" : share.share ,
                    "title" : share.title ,    
                    "tag" : share.tag ,    
                    "author_id" : share.author_id ,
                    "id" :  share.id , 
                    }
               ,201 ,  {'Location': url_for('api.get_shares' , \
                 _external=True)} ) 
 

@api.route('/delete/<int:id>',methods=['DELETE'])
def delete(id) :
    share = Share.query.get_or_404(id)
    token = request.headers.get("token")
    current_user_id = User.verify_auth_token(token).id
    author_id = Share.query.filter_by(id=id).first().author_id
    if  current_user_id == author_id :
        db.session.delete(share)
        db.session.commit()
        return jsonify({
            'deleted' : share.id  , 

            }) , 200 
    return jsonify({
        
        'message' : 'You can not delete it!'
        }) , 400



@api.route('/edit-share/<int:id>', methods=["PUT"])
def edit(id) :
    share = Share.query.get_or_404(id) 
    token = request.headers.get("token")
    current_user_id = User.verify_auth_token(token).id
    author_id = Share.query.filter_by(id=id).first().author_id
    if  current_user_id == author_id :
        share.share = request.get_json().get("share")
        share.title = request.get_json().get("title")
        db.session.add(share)
        db.session.commit()
        return jsonify({
            'edited' : share.id  ,
            }) , 200 
    return jsonify({ 
        
        'message' : 'You can not edit!'
        }) , 400 


@api.route('/',methods=['GET'])
def index() :
    page = request.args.get('page',1,type=int) 
    shares = {}

    sort_arg = request.args.get("sort")
    if sort_arg == None :
        shares_pages = \
        Share.query.order_by('-id').paginate(page,current_app.config['SHARE_PER_PAGE'],False)
        shares = shares_pages.items 

    elif sort_arg == "new" :
        shares_pages = Shares_pages = \
        Share.query.order_by('-id').paginate(page,currnet_app.config['SHAER_PER_PAGE'],False)
        shares = shares_pages.items

    elif sort_args == "hot" :
        shares = []
        for share in Share.query.all():
            shares_count[share] = share.comment.count()
        shares_count = sorted(shares_count.items(), lambda x ,y : cmp(y[1],x[1]))
        for tuple_ in shares_count :
            shares.append(tuple_[0])
        shares = shares[:5]
        shares_pages = None

    elif sort_args in tags :
        shares = []
        item = Share.query.filter_by(tag=sort_arg)
        shares_pages = \
        item.order_by('-id').pagniate(page,current_app.config['SHARE_PER_PAGE'],False)
        shares = shares_pages.items 

                        

    return jsonify({
            'page' : page , 
            'share' : [share.to_json() for share in shares ] , 
            }) , 200 
    
