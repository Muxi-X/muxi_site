# coding: utf-8

from . import blogs
from flask import render_template, render_template_string, redirect, url_for
from flask_login import current_user, login_required
from ..models import Blog, Comment
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
    blog_list = Blog.query.all()
    for blog in blog_list:
        blog.img_url = "http://7xj431.com1.z0.glb.clouddn.com/1-140G2160520962.jpg"
        blog.date = blog.timestamp
        blog.like_number = 1
        # blog.comment_number = 1
        blog.avatar = "http://7xj431.com1.z0.glb.clouddn.com/1-140G2160520962.jpg"
        blog.content = blog.body
    return render_template("pages/index.html", blog_list=blog_list)


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
        comment.date = comment.timestamp
        comment.content = comment.comment
    return render_template("pages/post.html", blog=blog, form=form, comment_list=comment_list)
