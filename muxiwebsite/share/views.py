# coding: utf-8

"""
    views.py ~ 木犀分享视图文件

        主页: 发布分享

        /:  主页
        /share:  发布分享的页面
        /login:  登录页
        /logout: 登出页
        /new: 显示最新分享
        /hot: 显示最热分享
        /view_share: 查看分享的具体信息，评论，发表评论
"""

# models import
from . import shares
from jinja2 import Environment
from .forms import ShareForm, CommentForm, EditForm
from .. import  db, app
from ..models import Share, Comment, User, Permission
from flask import url_for, render_template, redirect, request, current_app, Markup , jsonify , g
from flask_login import current_user, login_required
from ..decorators import permission_required , login_required
from ..login import Login
from ..signup import Signup
from sqlalchemy import desc
from sqlalchemy import func
import markdown
import json
import requests
import os
import pickle


tags2 = {'frontend' : ' 前端', 'backend' : '后端', 'android':'安卓','desgin':'设计','product':'产品'}
tags = ['frontend', 'backend', 'android', 'design', 'product']

@shares.route('/')
def index():
    """
    muxi_share 分享你的知识
	主页，默认显示最新的分享
	添加分页，默认显示第一页
    """

    flag = 0
    # 添加分页, share变为分页对象
    page = int(request.args.get('page') or 1)
    shares_count = {}
    # tags = ['frontend', 'backend', 'android', 'design', 'product']

    sort_arg = request.args.get('sort')
    if sort_arg == None:
        shares_pages = Share.query.order_by('-id').paginate(page, app.config['SHARE_PER_PAGE'], False)
        shares = shares_pages.items

    elif sort_arg == "new":
        flag = 0
        shares_pages = Share.query.order_by('-id').paginate(page, app.config['SHARE_PER_PAGE'], False)
        shares = shares_pages.items

    elif sort_arg == "hot":
        flag = 1
        shares = []
        for share in Share.query.all():
            shares_count[share] = share.comment.count()
        shares_count = sorted(shares_count.items(), lambda x, y: cmp(y[1], x[1]))
        for share_tuple in shares_count:
            shares.append(share_tuple[0])
        shares = shares[:5]
        shares_pages = None

    elif sort_arg in tags:
        flag = tags.index(sort_arg) + 2
        shares = []
        this_arg =  Share.query.filter_by(tag=sort_arg)
        shares_pages = this_arg.order_by('-id').paginate(page, app.config['SHARE_PER_PAGE'], False)
        shares = shares_pages.items


    for share in shares:
        share.avatar = User.query.filter_by(id=share.author_id).first().avatar_url
        share.comment_count = share.comment.count()
        share.author_id = share.author_id
        share.author = User.query.filter_by(id=share.author_id).first().username

    return render_template('share_index.html', tags = tags, shares=shares, flag=flag, Permission=Permission, shares_pages=shares_pages)


@shares.route('/view/<int:id>/', methods=["GET", "POST"])
def view_share(id):

    """
    显示特定id的分享，相关信息以及评论
    实现评论表单发表自己的评论
    """
    share = Share.query.get_or_404(id)
    share.author = User.query.filter_by(id=share.author_id).first().username
    comments = Comment.query.filter_by(share_id=share.id).all()
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(
            comment = form.comment.data,
            author_id = current_user.id,
            author_name = User.query.filter_by(id=current_user.id).first().username,
            share_id = id,
			count = 0
            )
        db.session.add(comment)
        db.session.commit()
        this_comment = Comment.query.filter_by(
			comment=form.comment.data,
			author_id=current_user.id,
			share_id = id,
			).first()
        this_comment.count += 1
        return redirect(url_for('shares.view_share', id=id))

    share.avatar =  User.query.filter_by(id=share.author_id).first().avatar_url
    share.comments = len(Comment.query.filter_by(share_id=share.id).all())

    for comment in comments:
        comment.avatar = User.query.filter_by(id=comment.author_id).first().avatar_url
        comment.username = User.query.filter_by(id=comment.author_id).first().username
        comment.content = comment.comment
    return render_template(
        'share_second.html',
        form = form,
        share = share,
        comments = comments
        )


@login_required
@shares.route('/send/', methods=["GET", "POST"])
def add_share():
    """
    分享
    """
    form = ShareForm()
    if form.validate_on_submit():
        share = Share(
                title = form.title.data,
                share = form.share.data,
                tag = form.tag.data,
                author_id = current_user.id
                )
        db.session.add(share)
        db.session.commit()
        share_tag = tags2[share.tag]
        link  = {
            "msgtype" : "link" ,
                "link" : {
                "title" : share.title ,
                "text" : share.share[:10]  ,
                "picUrl": "" ,
                "messageUrl" : url_for("shares.view_share",id=share.id,_external=True) ,
                }
            }
        headers = { "Content-Type" : "application/json" }
        try :
            r = requests.post(current_app.config['SEND_URL'],data=json.dumps(link),headers=headers)
        except :
            pass
        return redirect(url_for('.index', page = 1))
    return render_template("share_send.html", form=form, tags = tags)


@login_required
@shares.route('/delete/<int:id>/', methods=["GET", "POST"])
@permission_required(Permission.WRITE_ARTICLES)
def delete(id):
    """
    User could delete his share
    """
    share = Share.query.filter_by(id=id).first()
    db.session.delete(share)
    db.session.commit()
    return redirect(url_for("shares.index"))


@shares.route('/edit-share/<int:id>/', methods=["POST", "GET"])
@login_required
@permission_required(Permission.WRITE_ARTICLES)
def edit(id):
    """
    用户可以修改自己的分享
    """
    form = EditForm()
    share = Share.query.filter_by(id=id).first()
    if form.validate_on_submit():
        share.title = form.title.data
        share.share = form.share.data
        share.tag = form.tag.data
        db.session.add(share)
        db.session.commit()
        return redirect(url_for("shares.index", page=1))
    form.title.data = share.title
    form.share.data = share.share
    form.tag.data = share.tag
    return render_template(
            "edit-share.html",
            form = form,
            tags = tags
            )


@shares.route('/api/v2.0/all/', methods=['GET'])
def get_shares2():
    """
    获取所有分享
    """
    page = request.args.get('page', 1, type=int)
    pagination = Share.query.order_by('-id').paginate(
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


@shares.route('/api/v2.0/<int:id>/comments/',methods=["GET"])
def view_share2(id) :
    '''
    查看某一篇分享的评论
    '''
    share = Share.query.get_or_404(id)
    comments = Comment.query.order_by('-id').filter_by(share_id=id).all()

    return jsonify({
        "comment" :  [ comment.to_json() for comment in comments ] ,
        "comment_num" : len(comments) ,
        }) ,200

@shares.route('/api/v2.0/<int:id>/add_comment/',methods=['POST'])
@login_required
def add_comment2(id) :
    '''
    登录用户发表评论
    '''
    share = Share.query.filter_by(id=id).first()
    share.read_num = 1
    db.session.add(share)
    db.session.commit()
    comment = Comment()
    comment.comment = pickle.dumps(request.get_json().get("comment"))
    comment.share_id = id
    comment.author_id = g.current_user.id
    comment.author_name = g.current_user.username
    db.session.add(comment)
    db.session.commit()
    return jsonify({
        'message' : 'You add a comment successfully!'
        }) , 200


@shares.route('/api/v2.0/send/',methods=['POST'])
@login_required
def add_share2() :
    '''
    登录用户发送分享
    '''
    share = Share()
    share.title =  pickle.dumps(request.get_json().get("title"))
    share.share = pickle.dumps(request.get_json().get("share"))
    share.tag = request.get_json().get("tags")
    share.read_num = 0
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
                "messageUrl" : url_for("shares.views2",id=share.id,_external=True) ,
                }
            }

    headers = { "Content-Type" : "application/json" }
    try :
        r = requests.post(current_app.config['SEND_URL'],data=json.dumps(link),headers=headers)
    except :
        pass
    return jsonify( {
                    "share" : pickle.loads(share.share) ,
                    "title" : pickle.loads(share.title)  ,
                    "tag" : share.tag ,
                    "author_id" : share.author_id ,
                    "id" :  share.id ,
                    } ) , 200

@shares.route('/api/v2.0/<int:id>/delete/',methods=['DELETE'])
@login_required
def delete2(id) :
    '''
    删除分享(发送分享的用户)
    '''
    share = Share.query.get_or_404(id)
    if g.current_user.id != share.author_id :
        return jsonify({ }) , 403
    db.session.delete(share)
    db.session.commit()
    return jsonify({
            'deleted' : share.id  ,
            }) , 200

@shares.route('/api/v2.0/<int:id>/views/',methods=['GET'])
def views2(id) :
    '''
    查看单个分享,和它所有的评论
    '''
    share = Share.query.get_or_404(id)
    comments = Comment.query.order_by('-id').filter_by(share_id=id).all()
    return jsonify ({
        'share' : share.to_json() ,
        'comments' : [ comment.to_json() for comment in comments ] ,
        }) ,200

@shares.route('/api/v2.0/<int:id>/edit/', methods=["PUT"])
@login_required
def edit2(id) :
    '''
    编辑已经发送的分享(发送该分享的用户)
    '''
    share = Share.query.get_or_404(id)
    if g.current_user.id != share.author_id :
        return jsonify({ }) , 403
    share.share = pickle.dumps(request.get_json().get("share"))
    share.title = pickle.dumps(request.get_json().get("title"))
    db.session.add(share)
    db.session.commit()
    return jsonify({
            'edited' : share.id  ,
            }) , 200


@shares.route('/api/v2.0/',methods=['GET'])
def index2() :
    '''
    分享首页,根据所选标签显示分享
    '''
    page = request.args.get('page',1,type=int)
    sort_args = request.args.get("sort")
    if sort_args == None :
        shares_pages = \
        Share.query.order_by('-id').paginate(page,current_app.config['SHARE_PER_PAGE'],False)
        pages_count = shares_pages.total / current_app.config['SHARE_PER_PAGE']
        if shares_pages.total % current_app.config['SHARE_PER_PAGE'] != 0 :
            pages_count = pages_count + 1
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
        shares_pages = item.order_by('-id').paginate(page,current_app.config['SHARE_PER_PAGE'],False)
        pages_count = shares_pages.total / current_app.config['SHARE_PER_PAGE'] + 1
        shares = shares_pages.items
        if page > pages_count :
            return jsonify({
                'message' : 'can not find the page!'
                }) , 404

    share_num = len(shares)
    if share_num == 0 :
        return jsonify({ }) , 404

    return jsonify({
            'pages_count' : pages_count ,
            'page' : page ,
            'share' : [share.to_json() for share in shares ] ,
            'share_num' : share_num ,
     }) , 200

@shares.route('/api/v2.0/login/',methods=['POST'])
def login_for_share() :
    """
    登陆
    """
    username  = request.get_json().get("username")
    pwd = request.get_json().get("password")
    l = Login(username,pwd)
    res = l.login()
    if res[1] == 200 :
        return jsonify ({
            'token' : res[0] ,
            "avatar" : User.query.filter_by(username=username).first().avatar_url ,
            'user_id' : User.query.filter_by(username=username).first().id
            }) , res[1]
    return jsonify ({ }) , res[1]

@shares.route('/api/v2.0/signup/',methods=['POST'])
def signup_for_share() :
    """
    注册
    """
    un = request.get_json().get("username")
    password = request.get_json().get("password")
    s = Signup(un,password)
    res =  s.signup()
    if res[1] == 200 :
        return jsonify ({
            'created': res[0] ,
            }) , res[1]
    return jsonify({ }) , res[1]

@shares.route('/api/v2.0/get_some/',methods=['GET'])
def get_some() :
    """
    获取某些数量的分享
    """
    num =   request.args.get("num",type=int)
    shares = Share.query.order_by("-id").all()
    real_num = len(shares)
    if real_num >= num  :
        shares = shares[:num]

    return jsonify({
        'real_num' : real_num ,
        'shares' : [ share.to_json() for share in shares ]
        }) , 200

@shares.route('/api/v2.0/change_avatar/',methods=['POST'])
@login_required
def change_avatar() :
    """
    修改share里的头像
    """
    avatar = request.get_json().get("avatar")
    user = g.current_user
    user.avatar_url = avatar
    db.session.add(user)
    db.session.commit()
    return jsonify({
        "changed" : user.id ,
        }) , 200

@shares.route('/api/v2.0/get_one_all/',methods=['GET'])
@login_required
def get_one_all() :
    """
    获取某用户的所有的分享
    """
    ID = g.current_user.id
    shares = Share.query.filter_by(author_id=ID).all()
    return jsonify({
            'share_num' : len(shares) ,
            'shares' : [ item.to_json3() for item in shares ] ,
        }) , 200

@shares.route('/api/v2.0/<int:id>/read_comment/',methods=['POST'])
@login_required
def read_comment(id) :
    """
    将某篇分享的评论设为已读
    """
    share = Share.query.filter_by(id=id).first()
    if g.current_user.id != share.author_id :
        return jsonify({ }) , 403
    share.read_num = 0  # 已读为0，未读为1
    db.session.add(share)
    db.session.commit()
    return jsonify({ }) , 200
