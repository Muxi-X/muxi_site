# coding: utf-8

from . import blogs
from flask import render_template, render_template_string, redirect, url_for, request, \
        current_app
from flask_login import current_user, login_required
from sqlalchemy import desc
from ..models import Blog, Comment, Tag, User, Type
from .forms import CommentForm
from muxiwebsite import db, auth


@blogs.route('/')
def index():
    """
    木犀博客首页
    """
    page = int(request.args.get('page') or 1)
    article_tag = Tag.query.all()
    blog_all = Blog.query.order_by('-id').all()
    blog_list = Blog.query.order_by('-id').paginate(page, current_app.config['BLOG_PER_PAGE'], False)
    for blog in blog_all:
        blog.date = str(blog.timestamp)[:-3]
        blog.avatar = User.query.filter_by(id = blog.author_id).first().avatar_url
        blog.content = blog.body
    article_date = []

    for blog in blog_all:
        if blog.index not in article_date:
            article_date.append(blog.index)

    return render_template("pages/index.html", blog_list=blog_list,
                           article_tag=article_tag, article_date=article_date)


@blogs.route('/index/<string:index>/', methods=["GET"])
def ym(index):
    """
    博客归档页面
    :return:
    """
    blog_list = []
    for blog in Blog.query.all():
        if blog.index == index:
            blog_list.append(blog)
    for blog in blog_list:
        blog.date = str(blog.timestamp)[:-3]
        blog.avatar = User.query.filter_by(id=blog.author_id).first().avatar_url
        blog.content = blog.body
    article_date = []
    for blog in Blog.query.all():
        if blog.index not in article_date:
            article_date.append(blog.index)
    return render_template('pages/archive.html', blog_list=blog_list,
            index=index, article_date=article_date)


@blogs.route('/post/<int:id>/', methods=["POST", "GET"])
@login_required
def post(id):
    """
    博客文章页面
    """
    form = CommentForm()
    blog = Blog.query.get_or_404(id)
    blog.content = blog.body
    if form.validate_on_submit():
        # 提交评论
        comment = Comment(
            comment=form.comments.data,
            # count=len(blog.)+1,
            author_id=current_user.id,
            blog_id=id
        )
        db.session.add(comment)
        db.session.commit()

        blog.comment_number += 1
        db.session.add(blog)
        db.session.commit()
        return redirect(url_for('blogs.post', id=id))

    comment_list =Comment.query.filter_by(blog_id=id).all()
    for comment in comment_list:
        comment.date = str(comment.timestamp)[:-3]
        comment.content = comment.comment
    return render_template("pages/post.html", blog=blog, form=form, comment_list=comment_list)


@blogs.route('/<string:type>/')
def types(type):
    """
    返回对应分类下的文章
    分类: WEB, 设计, 安卓, 产品, 关于
    """
    page = int(request.args.get('page') or 1)
    blog_all = Blog.query.all()
    type_item = Type.query.filter_by(value=type).first()
    blog_list = Blog.query.filter_by(type_id=type_item.id).paginate(page, current_app.config['BLOG_PER_PAGE'], False)
    for blog in blog_all:
        blog.date = str(blog.timestamp)[:-3]
        blog.avatar = User.query.filter_by(id=blog.author_id).first().avatar_url
        blog.content = blog.body

    article_date = []
    for blog in blog_all:
        if blog.index not in article_date:
            article_date.append(blog.index)

    return render_template('pages/type.html', blog_list=blog_list, type=type,
            article_date=article_date)

