# coding: utf-8
from . import blogs
from flask import render_template, render_template_string, redirect, url_for, request, \
        current_app
from flask_login import current_user, login_required
from sqlalchemy import desc
from ..models import Blog, Comment, Tag, User, Type
from .forms import CommentForm
from muxiwebsite import db, auth

# 木犀博客首页
@blogs.route('/',methods=['GET'])
def index():
    page = int(request.args.get('page') or 1)
    article_tag = Tag.query.all()
    blog_all = Blog.query.order_by('-id').all()
    blog_list = Blog.query.order_by('-id').paginate(page, current_app.config['BLOG_PER_PAGE'], False)
    for blog in blog_all:
        blog.date = "%d/%02d/%02d" % (blog.timestamp.year, blog.timestamp.month, blog.timestamp.day)
        try:
            blog.avatar = User.query.filter_by(id=blog.author_id).first().avatar_url
        except AttributeError:
            blog.avatar = ""
        blog.content = blog.body
        blog.intro = blog.summary
    article_date = []

    for blog in blog_all:
        if blog.index not in article_date:
            article_date.append(blog.index)

    return jsonify({
                   'blog_list':blog_list,
                   'article_tag':article_tag,
                   'article_date':article_date,
                   'blog_avatar':blog_avatar,
                   'blog_body':blog_body}) , 200

#博客归档页面return:
@blogs.route('/index/<string:index>/', methods=["GET"])
def ym(index):
   
    blog_list = []
    for blog in Blog.query.all():
        if blog.index == index:
            blog_list.append(blog)
    for blog in blog_list:
        blog.date = "%d/%02d/%02d" % (blog.timestamp.year, blog.timestamp.month, blog.timestamp.day)
        blog.avatar = User.query.filter_by(id=blog.author_id).first().avatar_url
        blog.content = blog.body
    article_date = []
    for blog in Blog.query.all():
        if blog.index not in article_date:
            article_date.append(blog.index)
    return jsonify({
                   'blog_list':blog.list,
                   'index':blog.index,
                   'article_date':article.date
                   'blog_avatar'=blog.avatar,
                   'blog_content' = blog.body}) , 200


#博客文章页面
@blogs.route('/post/<int:id>/', methods=["POST", "GET"])
def post(id):
    blog = Blog.query.get_or_404(id)
    blog.content = blog.body
    blog.date = "%d年%d月%d日 %d:%d" % (blog.timestamp.year,
            blog.timestamp.month, blog.timestamp.day, blog.timestamp.hour,
            blog.timestamp.minute)
    if request.method == 'POST' :
        # 提交评论
        if current_user.is_authenticated:
            name = current_user.username
            uid = current_user.id
        else:
            name = form.username.data
            uid = 0
            comment = Comment()
            comment.comment =request.get_json().get("comment")
            comment.author_id= request.get_json().get("uid")
            comment.author_name =  request.get_json().get("name")
            comment.blog_id= request.get_json().get("id")

            db.session.add(comment)
            db.session.commit()

            blog.comment_number += 1
            db.session.add(blog)
            db.session.commit()

    return jsonify(comment.to_json()) , 201

    comment_list =Comment.query.filter_by(blog_id=id).all()
    for comment in comment_list:
        comment.date = str(comment.timestamp)[:-10]
        comment.content = comment.comment
    return jsonify({
                   'blog':blog.blog,
                   'author_id':comment.author_id,
                   'blog_id':comment.blog_id,
                   'author_id':comment.author_name;
                   'list':comment_list,
                   'comment': [comment.to_json() for comment in comment_list ]}) , 200

#  返回对应分类下的文章,分类: WEB, 设计, 安卓, 产品, 关于
@blogs.route('/type/<string:type>/',methods=['GET'])
def types(type):

    page = int(request.args.get('page') or 1)
    blog_all = Blog.query.all()
    type_item = Type.query.filter_by(value=type).first()
    blog_list = Blog.query.filter_by(type_id=type_item.id).paginate(page, current_app.config['BLOG_PER_PAGE'], False)
    for blog in blog_all:
        blog.date = "%d/%02d/%02d" % (blog.timestamp.year, blog.timestamp.month, blog.timestamp.day)
        blog.avatar = User.query.filter_by(id=blog.author_id).first().avatar_url
        blog.content = blog.body

    article_date = []
    for blog in blog_all:
        if blog.index not in article_date:
            article_date.append(blog.index)

    return jsonify({
                   'blog_list':blog_list,
                   'type_item':type_item,
                   'page'=page,
                   'article_date':article_date}) , 200
