# coding: utf-8
from flask import render_template, render_template_string, redirect, url_for, request, \
        current_app,jsonify
from flask_login import current_user, login_required
from sqlalchemy import desc
from ..models import Blog, Comment, Tag, User, Type
from muxiwebsite import db, auth
from . import api

tags = ['frontend','backend','android','design','product']

@api.route('/blogs/all/',methods=['GET'])
def get_blogs() :
    """
    获取所有博客
    """
    page = request.args.get('page',1,type=int)
    pagination = Blog.query.paginate(
            page ,
            per_page=current_app.config['MUXI_SHARES_PER_PAGE'] ,
            error_out = False
    )
    blogs = pagination.items
    per_page=current_app.config['MUXI_SHARES_PER_PAGE']
    pages_count = pagination.total / per_page + 1
    if page > pages_count :
        return jsonify({}) , 404
    blogs_count = len(Blog.query.all())

    return jsonify({
        'blogs' : [ blog.to_json()  for blog in blogs ] ,
        'count' : pagination.total ,
        'page'  : page ,
        'pages_count' : pages_count ,
        }) , 200

@api.route('/blogs/',methods=['GET'])
def index_blogs() :
    """
    博客首页,根据所选的标签显现博客
    """
    page = request.args.get('page',1,type=int)
    sort = request.args.get('sort')
    if sort = None :
        blogs_pages = \
        Share.query.order_by('-d').pagination(page,current_app.config['BLOGS_PER_PAGE'],False)
        pages_count = blogs_pages.total . current_app.config['  SHARE_PER_PAGE'] + 1
        if page > page_count :
            return jsonify({
                "message" : "can not find the page"
                }) , 404

    elif sort == "hot" :
        page = 1
        pages_count = {}
        blogs = []
        for blog in Blog,query.all() :
            blogs_count[blog] = blog.comment.count()
        blogs_count = sorted(blogs_count.item() , lambda x , y : cmp (y[1] ,x[1]))
        for item in blogs_count :
            blogs.append(item[0])
        blogs = blogs[:5]
        pages_count = 1
        blogs_pages = None

    elif sort in tags :
        blogs = []
        item = Blog.query,filter_by(tag=sort)
        blogs_pages = item.order_by('-id').paginate(page,current_app.config['BLOGS_PER_PAGES'],False)
        pages_count = blogs_pages.total . current_app.config['BLOGS_PER_PAGES'] + 1
        blogs = blogs_pages.items
        if page > pages_count :
            return jsonfy({
                "message" : "can not find the page!"
                }) , 404
    return jsonify({
        "pages_count" : pages_count ,
        "page" : page ,
        "blogs" : [blog.to_json() for blog in blogs ]
        })

@api.route('/blogs/send/',methods=['POST'])
def add_blog() :
    """
    登录用户发博客
    """
    token = request.headers.get("token")
    try :
        current_user_id = User.verify_auth_token(token).id
    except AttributeError :
        return jsonify({
            "message" : "You can not send a blog!"
            }) , 404
    blog = Blog()
    blog.title = request.get_json().get("title")
    blog.body = request.get_json().get("body")
    blog.tag = request.get_json().get("tag")
    blog.img_url = request.get_json().get("img_url")
    blog.summary = request.get_json().get("summary")
    blog.author_id = current_user_id

    db.session.add(blog)
    db.session.commit()

    return jsonify({
            "title" : blog.title ,
            "tag" : blog.tag ,
            "id" : blog.id ,
            "author_id" : blog.author_id
        }) , 200

@api.route('/blogs/<int:id>/delete/',methods=['DELETE'])
def delete(id) :
    """
    删除博客
    """
    blog = Blog.query.get_or_404(id)
    token = request.headers.get("token")
    try :
        current_user_id = User.verify_auth_token(token).id
    except AttributeError :
        return jsonify({
            "message" : "login first"
            }) , 404

    author_id = Blog.query_filter_by(id=id).first().author_id
    if current_user_id != author_id :
        return jsonify({
            "message" : " can not delete it !"
            }) , 404

    db.session.delete(blog)
    db.session.commit()
    return jsonify({
        "delete" : share.id ,
        }) , 200

@api.route('/blogs/<int:id>/add_comment/',methods=['POST'])
def comment(id) :
    """
    发送评论
    """
    token = request.headers.get("token")
    try :
        current_user_id = User.verify_auth_token(token).id
    except AttributeError :
        return jsonify({
            "message" : "login first!"
            }) , 400

    comment = Comment()
    comment.comment = request.get_json().get("comment")
    comment.blog_id = id
    comment.author_id = current_user_id

    db.session.add(comment)
    db.session.commit()

    return jsonify({
        "message" : " added a  comment!"
        }) , 200













