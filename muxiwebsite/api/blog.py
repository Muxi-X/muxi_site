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

@api.route('/blogs/',methods=['GET'])
def get_blogs() :
    """
    获取所有博客
    """
    page = request.args.get('page',1,type=int)
    blog_list = Blog.query.order_by('-id').paginate(page,current_app.config['BLOG_PER_PAGE'],False)
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

@api.route('/blogs/sort/',methods=['GET'])
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
    blog.type_id = request.get_json().get("type_id")
    tag2 = request.get_json().get("tags")

    db.session.add(blog)
    db.session.commit()

    for item in tag2 :
        tag = Tag.query.filter_by(value=str(item)).first()
        if tag is None :
            blogs = Blog.query.filter_by(id=blog.id).all()
            tag = Tag(
                blogs = blogs ,
                value = str(item) ,
            )
        else :
            blogs = Tag.query.filter_by(value=item).first().blogs
            blogs.append(blog)
            tag.blogs = set(blogs)
        db.session.add(tag)
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

@api.route("/blogs/<int:id>/add_tag/",methods=['POST'])
@login_required
@permission_required(Permission.WRITE_ARTICLES)
def add_tag(id) :
    """
    添加标签
    """
    tag = request.get_json().get("tag")
    tags = Tag.query.filter_by(value=tag).first()
    if  tags is None :
        blog = Blog.query.filter_by(id=id).all()
        tags = Tag(
                blogs = blog ,
                value = tag
            )
    else :
        blog = Blog.query.filter_by(id=id).first()
        blogs = tags.blogs
        blogs.append(blog)
        tags.blogs = set(blogs)
    db.session.add(tags)
    db.session.commit()
    return jsonify({
    "tag" : tags.value ,
    }) , 200

@api.route('/blogs/<int:id>/view_tags/',methods=['GET'])
def view_tag(id) :
    """
    查看某一篇博客的所有标签
    """
    tag = Blog.query.filter_by(id=id).first().tags
    return jsonify({
        "tag_num" : len(list(tag)) ,
        "tags" : [ item.value for item in tag ]  ,
        })  ,  200

@api.route('/blogs/<string:tag>/find_blogs/',methods=['GET'])
def find_tag(tag) :
    """
    查看某种标签的所有博客
    """
    blogs = Tag.query.filter_by(value=tag).first().blogs
    return jsonify({
        "blog_num" : len(list(blogs)) ,
        "blogs" : [ item.to_json() for item in blogs ] ,
        }) , 200


@api.route('/blogs/<int:id>/edit/',methods=['PUT'])
@login_required
@permission_required(Permission.WRITE_ARTICLES)
def edit_blog(id) :
    """
    登录用户修改
    """
    blog = Blog.query.filter_by(id=id).first()
    blog.title = request.get_json().get("title")
    blog.body = request.get_json().get("body")
    blog.img_url = request.get_json().get("img_url")
    blog.summary = request.get_json().get("summary")
    blog.type_id = request.get_json().get("type_id")
    tag2 = request.get_json().get("tags")

    db.session.add(blog)
    db.session.commit()

    for item in tag2 :
        tag = Tag.query.filter_by(value=str(item)).first()
        if tag is None :
            blogs = Blog.query.filter_by(id=blog.id).all()
            tag = Tag(
                blogs = blogs ,
                value = str(item) ,
            )
        else :
            blogs = Tag.query.filter_by(value=item).first().blogs
            blogs.append(blog)
            tag.blogs = set(blogs)
        db.session.add(tag)
        db.session.commit()

    return jsonify({
            "id" : blog.id ,
            "author_id" : blog.author_id
        }) , 200


