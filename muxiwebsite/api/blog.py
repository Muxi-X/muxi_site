# coding: utf-8
from flask import render_template, render_template_string, redirect, url_for, request, \
        current_app,jsonify , g
from flask_login import current_user, login_required
from sqlalchemy import desc
from ..models import Blog, Comment, Tag, User, Type , Permission
from muxiwebsite import db, auth
from . import api
from .decorators import login_required , permission_required

tags = ['frontend','backend','android','design','product']

@api.route('/blogs/all/',methods=['GET'])
def get_blogs() :
    """
    获取所有博客
    """
    page = request.args.get('page',1,type=int)
    blog_list = Blog.query.order_by('id').paginate(page,current_app.config['BLOG_PER_PAGE'],False)
    pages_count = len(Blog.query.all())/current_app.config['BLOG_PER_PAGE'] + 1
    if page > pages_count :
        return jsonify({}) , 404
    blogs_count = len(Blog.query.all())

    return jsonify({
        'blogs' : [ blog.to_json()  for blog in blog_list.items ] ,
        'count' : blogs_count ,
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
    item = Blog.query.filter_by(type_id=sort)
    blog_list = item.order_by('id').paginate(page,current_app.config['BLOG_PER_PAGE'],False)
    pages_count = blog_list.total/current_app.config['BLOG_PER_PAGE'] + 1
    if page > pages_count :
        return jsonify({
            "message" : "can not find the page"
            }) , 404
    blogs = blog_list.items
    return jsonify({
        "pages_count" : pages_count ,
        "page" : page ,
        "blogs" : [blog.to_json() for blog in blogs ]
        }), 200

@api.route('/blogs/send/',methods=['POST'])
@login_required
def add_blog() :
    """
    登录用户发博客
    """
    blog = Blog()
    blog.title = request.get_json().get("title")
    blog.body = request.get_json().get("body")
    blog.img_url = request.get_json().get("img_url")
    blog.summary = request.get_json().get("summary")
    blog.author_id = g.current_user.id
    db.session.add(blog)
    db.session.commit()
    return jsonify({
            "id" : blog.id ,
            "author_id" : blog.author_id
        }) , 200

@api.route('/blogs/<int:id>/delete/',methods=['DELETE'])
@login_required
@permission_required(Permission.WRITE_ARTICLES)
def deleted(id) :
    """
    删除博客
    """
    blog = Blog.query.get_or_404(id)
    db.session.delete(blog)
    db.session.commit()
    return jsonify({
        "delete" : blog.id ,
        }) , 200

@api.route('/blogs/<int:id>/add_comment/',methods=['POST'])
@login_required
def comment(id) :
    """
    发送评论
    """
    comment = Comment()
    comment.comment = request.get_json().get("comment")
    comment.blog_id = id
    comment.author_id = g.current_user.id

    db.session.add(comment)
    db.session.commit()

    return jsonify({
        "message" : " added a  comment!"
        }) , 200


@api.route('/blogs/<int:id>/comment/',methods=['GET'])
def view_comment(id) :
    """
    查看评论
    """
    comments= Comment.query.filter_by(blog_id=id).all()
    return jsonify({
        'comments' : [ comment.to_json() for comment in comments ] ,
        })  , 200


@api.route('/blogs/<int:id>/views/',methods=['GET'])
def view(id) :
    """
    查看单个博客和他的评论
    """
    blog = Blog.query.get_or_404(id)
    comments= Comment.query.filter_by(blog_id=id).all()
    return jsonify({
        'comments' : [ comment.to_json() for comment in comments ] ,
        'blog' : blog.to_json()
        })  , 200


