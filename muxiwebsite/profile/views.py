# coding: utf-8
"""
    views.py
    ~~~~~~~~

    木犀个人页视图

"""

from . import profile
from flask import render_template, url_for, redirect
from ..models import User
from .forms import EditForm
from muxiwebsite import db


@profile.route('/<int:id>/')
def user_profile(id):
    """
    ex: /profile/1/
    木犀个人页
    """
    user = User.query.get_or_404(id)
    user.avatar = "http://7xj431.com1.z0.glb.clouddn.com/20150629_182823.jpg"
    blogs = user.blogs
    for blog in blogs:
        blog.address = url_for('blogs.post', id=blog.id)

    books = user.book
    for book in books:
        book.title = book.name
        book.date = book.end

    shares = user.share # topic, author, contents
    for share in shares:
        share.topic = share.title
        share.author = user.username
        share.contents = share.share[:10]

    return render_template(
        "pages/user.html",
        user=user,
        blogs=blogs,
        books=books,
        shares=shares
    )


@profile.route('/<int:id>/edit/', methods=['GET', 'POST'])
def edit(id):
    """
    编辑个人页
    """
    user = User.query.filter_by(id=id).first()
    form = EditForm()
    if form.validate_on_submit():
        user.username = form.username.data
        user.avatar_url = form.avatar_url.data
        user.info = form.info.data
        user.personal_blog = form.personal_blog.data
        user.github = form.github.data
        user.flickr = form.flickr.data
        user.weibo = form.weibo.data
        user.zhihu = form.zhihu.data
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('.user_profile', id=id))
    return render_template('/pages/edit.html', form=form)

