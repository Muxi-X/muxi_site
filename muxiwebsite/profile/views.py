# coding: utf-8
"""
    views.py
    ~~~~~~~~

    木犀个人页视图

"""

from . import profile
from flask import render_template, url_for, redirect, request, flash
from flask.ext.login import current_user
from ..models import User, Book
from .forms import EditForm
from muxiwebsite import db


@profile.route('/<int:id>/', methods=["POST", "GET"])
def user_profile(id):
    """
    ex: /profile/1/
    木犀个人页
    """
    user = User.query.get_or_404(id)
    user.avatar = user.avatar_url
    blogs = user.blogs
    for blog in blogs:
        blog.address = url_for('blogs.post', id=blog.id)

    books = user.book
    #return render_template("test.html", books=books)
    for book in books:
        book.title = book.name
        book.date = book.end

    shares = user.share # topic, author, contents
    for share in shares:
        share.topic = share.title
        share.author = user.username
        share.contents = share.share[:10]

    if request.method == 'POST':
        book = Book.query.get_or_404(book.id)
        book.status = False
        book.start = None
        book.end = None
        book.user_id = None
        flash('《%s》已归还' % book.name)
        return redirect(url_for('profile.user_profile', id=current_user.id))

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
        return redirect(url_for('profile.user_profile', id=id))
    form.username.data = user.username
    form.avatar_url.data = user.avatar_url
    form.info.data = user.info
    form.personal_blog.data = user.personal_blog
    form.github.data = user.github
    form.flickr.data = user.flickr
    form.weibo.data = user.weibo
    form.zhihu.data = user.zhihu
    return render_template('/pages/edit.html', form=form)

