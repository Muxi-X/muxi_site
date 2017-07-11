# coding: utf-8

"""
    share.py
    ~~~~~~~~

    木犀分享的信息

"""

from flask import url_for, jsonify, request, g, current_app
from muxiwebsite.models import Share, AnonymousUser , User , Comment , Permission , db
from .authentication import auth
from flask_login import current_user
from .decorators import permission_required , login_required
from . import api
import requests
import json
import os

URL = os.environ.get("SEND_URL")
tags = list(['frontend', 'backend', 'android', 'design', 'product'])
tags2 = {'frontend' : ' 前端', 'backend' : '后端', 'android':'安卓','desgin':'设计','product':'产品'}

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
    shares_count = len(Share.query.all())

    return jsonify({
        'shares': [ share.to_json()  for share in shares ],
        'count': pagination.total ,
        'page' : page , # 当前页数
        'pages_count' : pages_count ,
    }), 200


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
@login_required
def add_comment(id) :
    '''
    登录用户发表评论
    '''
    comment = Comment()
    comment.comment = request.get_json().get("comment")
    comment.share_id = id
    comment.author_id = g.current_user.id
    db.session.add(comment)
    db.session.commit()
    return jsonify({
        'message' : 'You add a comment successfully!'
        }) , 200


@api.route('/shares/send/',methods=['POST'])
@login_required
def add_share() :
    '''
    登录用户发送分享
    '''
    share = Share()
    share.title =  request.get_json().get("title")
    share.share = request.get_json().get("share")
    share.tag = request.get_json().get("tags")
    share.author_id = g.current_user.id
    db.session.add(share)
    db.session.commit()
    share_tag = tags2[share.tag]
    link  = {
            "msgtype" : "link" ,
            "link" : {
                "title" : share.title ,
                "text" : share.share[:10]  ,
                "picUrl": "" ,
                "messageUrl" : url_for("api.views",id=share.id,_external=True) ,
                }
            }

    headers = { "Content-Type" : "application/json" }
    r = requests.post(URL,data=json.dumps(link),headers=headers)
    return jsonify( {
                    "share" : share.share ,
                    "title" : share.title ,
                    "tag" : share.tag ,
                    "author_id" : share.author_id ,
                    "id" :  share.id ,
                    } ) , 200

@api.route('/shares/<int:id>/delete/',methods=['DELETE'])
@login_required
@permission_required(Permission.WRITE_ARTICLES)
def delete(id) :
    '''
    删除分享(发送分享的用户)
    '''
    share = Share.query.get_or_404(id)
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
@login_required
@permission_required(Permission.WRITE_ARTICLES)
def edit(id) :
    '''
    编辑已经发送的分享(发送该分享的用户)
    '''
    share = Share.query.get_or_404(id)
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
        Share.query.order_by('id').paginate(page,current_app.config['SHARE_PER_PAGE'],False)
        pages_count = shares_pages.total / current_app.config['SHARE_PER_PAGE'] + 1
        if page > pages_count :
            return jsonify({
                'message' : 'can not find the page!'
                }) , 404
        shares = shares_pages.items

    elif sort_args == "hot" :
        page = 1
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
        shares_pages = item.order_by('id').paginate(page,current_app.config['SHARE_PER_PAGE'],False)
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

