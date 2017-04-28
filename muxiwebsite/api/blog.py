# coding: utf-8
from flask import render_template, render_template_string, redirect, url_for, request, \
        current_app,jsonify
from flask_login import current_user, login_required
from sqlalchemy import desc
from ..models import Blog, Comment, Tag, User, Type
from muxiwebsite import db, auth
from . import api


@api.route('/blog/',methods=['GET'])
def get_blog():
    """
    木犀博客首页
    """
    page = int(request.args.get('page') or 1)
    article_tag = Tag.query.all()
    blog_all = Blog.query.order_by('-id').all()
    pagination = Blog.query.order_by('-id').paginate(page, current_app.config['BLOG_PER_PAGE'], False)
    blog_list = pagination.items
    for blog in blog_all:
        blog.date = "%d/%02d/%02d" % (blog.timestamp.year, blog.timestamp.month, blog.timestamp.day)
        try:
            blog.avatar = User.query.filter_by(id=blog.author_id).first().avatar_url
        except AttributeError:
            blog.avatar = ""
        blog.content = blog.body
        blog.intro = blog.summary
    article_date = []

    return jsonify([{
                   'blog_tag':blog.tag.value,
                   'blog_date':"%d/%02d/%02d" % (blog.timestamp.year, blog.timestamp.month, blog.timestamp.day),
                   'blog_avatar':User.query.filter_by(id=blog.author_id).first().avatar_url,
                   'blog_body':blog.body}
                    for blog in blog_list]) , 200


@api.route('/blog/index/<string:index>/', methods=["GET"])
def ym(index):
    """
    博客归档页面return:
    """
    blog_list = []
    for blog in Blog.query.all():
        if blog.index == index:
            blog_list.append(blog)
        article_date = []
    for blog in Blog.query.all():
        if blog.index not in article_date:
            article_date.append(blog.index)
    return jsonify([{
                   'index':blog.index,
                   'blog_date': "%d/%02d/%02d" % (blog.timestamp.year, blog.timestamp.month, blog.timestamp.day),
                   'blog_avatar':User.query.filter_by(id=blog.author_id).first().avatar_url,
                   'blog_content':blog.body}
                    for blog in blog_list]) , 200


@api.route('/blog/post/<int:id>/', methods=["GET"])
def post(id):
    """
    博客文章页面
    """
    blog = Blog.query.get_or_404(id)
    comment_list =Comment.query.filter_by(blog_id=id).all()
    return jsonify({
                   'body':blog.body,
                   'index':blog.index,
                   'author_id':blog.author_id,
                   'blog_id':blog.id,
                   'blog_date': "%d年%d月%d日 %d:%d" % (blog.timestamp.year,
                           blog.timestamp.month, blog.timestamp.day, blog.timestamp.hour,
                           blog.timestamp.minute),
                   'comment': [comment.to_json() for comment in comment_list ]}) , 200


@api.route('/blog/post/<int:id>/comments/', methods=["POST"])
def comment(id):

    """
    提交评论
    """
    if request.method == 'POST' :
        blog = Blog.query.get_or_404(id)
        comments = Comment.query.filter_by(blog_id=id).all()
        comment = Comment()
        comment.comment = request.get_json().get("comment")
        comment.blog_id = request.get_json().get("id")

        comment.author_id = request.get_json().get("author_id")
        db.session.add(comment)
        db.session.commit()
        blog.avatar = \
                User.query.filter_by(id=blog.author_id).first().avatar_url

        for comment in comments :
            comment.avatar = \
                User.query.filter_by(id=comment.author_id).first().avatar_url
            comment.username = \
                User.query.filter_by(id=comment.author_id).first().username
            comment.content  = comment.comment


        blog.comment_number += 1
        db.session.add(blog)
        db.session.commit()
        return jsonify(comment.to_json())

@api.route('/blog/type/<string:type>/',methods=['GET'])
def types(type):
    """
    返回对应分类下的文章,分类: WEB, 设计, 安卓, 产品, 关于
    """
    page = int(request.args.get('page') or 1)
    blog_all = Blog.query.all()
    type_item = Type.query.filter_by(value=type).first()
    pagination = Blog.query.filter_by(type_id=type_item.id).paginate(page, current_app.config['BLOG_PER_PAGE'], False)
    blog_list = pagination.items
    for blog in blog_all:
        blog.date = "%d/%02d/%02d" % (blog.timestamp.year, blog.timestamp.month, blog.timestamp.day)
        blog.avatar = User.query.filter_by(id=blog.author_id).first().avatar_url
        blog.content = blog.body

    article_date = []
    for blog in blog_all:
        if blog.index not in article_date:
            article_date.append(blog.index)

    return jsonify([{
                    'blog_tag':[t.value for t in blog.tags],
                    'blog_date':"%d/%02d/%02d" % (blog.timestamp.year, blog.timestamp.month, blog.timestamp.day),
                    'blog_avatar':User.query.filter_by(id=blog.author_id).first().avatar_url,
                    'blog_body':blog.body,
                    'type_item':type_item.value,
                    'page':page}
                    for blog in blog_list]) , 200  


@api.route('/blog/<int:id>/edit/' ,methods=['PUT'])
@login_required
def edit_blog(id) :
    '''
    编辑博客
    '''
    blog = Blog.query.get_or_404(id)
    token = request.headers.get("token")
    try :
        current_user_id = User.verify_auth_token(token).id
    except AttributeError :
        return jsonify({
            'message' : '抱歉请先登录'
            }) , 400
    type_id = Blog.query.filter_by(id=id).first().type_id
    author_id = Blog.query.filter_by(id=id).first().author_id
    if  current_user_id != author_id :
        return jsonify({
            'message': '抱歉你没有编辑的权限'
            }) , 404

    blog.body = request.get_json().get("body")
    blog.title = request.get_json().get("title")
    blog.summary = request.get_json().get("summary")

    db.session.add(blog)
    db.session.commit()
    return jsonify({
            'edited' : blog.id ,
            }) , 200


@api.route('/blog/send/',methods=['POST'])
def add_blog(id) :
    '''
    登录用户发送分享
    '''
    token = request.headers.get("token")
    try :
        current_user_id = User.verify_auth_token(token).id
    except AttributeError :
        return jsonify({
            'message' : '你不能添加博客'
            }) , 404

    blog = Blog()
    blog.title =  request.get_json().get("title")
    blog.body = request.get_json().get("body")
    blog.summary = request.get_json().get("summary")
    blog.tag = request.get_json().get("tags")
    blog.author_id = current_user_id

    db.session.add(blog)
    db.session.commit()

    return jsonify( {
                    "body" : blog.body ,
                    "title" : blog.title ,
                    "summary":blog.summary ,
                    "tag" : blog.tag ,
                    "author_id" : blog.author_id ,
                    "id" :  blog.id ,
                    } ) , 200 


@api.route('/blog/<int:id>/delete/',methods=['DELETE'])
def blog_delete(id) :
    blog = Blog.query.get_or_404(id)
    token = request.headers.get("token")
    try :
        current_user_id = User.verify_auth_token(token).id
    except AttributeError :
        return jsonify({
            'message': '请先登录'
            }) , 404

    author_id = Blog.query.filter_by(id=id).first().author_id
    if  current_user_id != author_id :
        return jsonify({
            'message' : '你没有权限删除该博客'
            }) , 404

    db.session.delete(blog)
    return jsonify({
            'deleted' : blog.id  ,
            }) , 200

