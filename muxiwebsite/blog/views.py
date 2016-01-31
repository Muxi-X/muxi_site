# coding: utf-8

from . import blogs
from flask import render_template, render_template_string, redirect, url_for
from flask_login import current_user, login_required
from sqlalchemy import desc
from ..models import Blog, Comment, Tag
from .forms import CommentForm
# from .. import muxi_root_path
# from jinja2 import FileSystemLoader
from muxiwebsite import db, auth


@blogs.route('/')
def index():
    """
    木犀博客首页
    blog_list: 博客文章的集合
    blog.img_url
    blog.name
    blog.date
    blog.like_number
    blog.comment_number
    for item in tag
    item.value
    blog.avatar
    """
    article_tag = Tag.query.all()
    blog_list = Blog.query.order_by('-id').all()
    for blog in blog_list:
        blog.date = str(blog.timestamp)[:-6]
        blog.like_number = 1
        # blog.comment_number = 1
        blog.avatar = "http://7xj431.com1.z0.glb.clouddn.com/1-140G2160520962.jpg"
        blog.content = blog.body
    article_date = []

    for blog in blog_list:
        if blog.index not in article_date:
            article_date.append(blog.index)

    return render_template("pages/index.html", blog_list=blog_list,
                           article_tag=article_tag, article_date=article_date)


@blogs.route('/index/<index>/', methods=["GET"])
def ym(index):
    """
    博客归档页面
    :return:
    """
    # blog_list = Blog.query.filter_by(index=index).all()
    blog_list = []
    for blog in Blog.query.all():
        if blog.index == index:
            blog_list.append(blog)
    return render_template('placeholder.html', blog_list=blog_list)


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
        comment.date = str(comment.timestamp)[:-6]
        comment.content = comment.comment
    return render_template("pages/post.html", blog=blog, form=form, comment_list=comment_list)


@blogs.route('/post/<int:id>/like/')
def like(id):
    """
    对特定id的文章点赞
    :param id:
    :return:
    """
    pass

@blogs.route('/test')
def test():
    return render_template('pages/base2.html')

