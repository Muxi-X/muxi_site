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
import datetime


@profile.route('/<int:id>/', methods=["POST", "GET"])
def user_profile(id):
    """
    ex: /profile/1/
    木犀个人页
    """
    date = datetime.date.today().strftime('%Y%m%d')[:4]
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
        for iid in request.form.values():
            book = Book.query.get_or_404(iid)
            book.status = False
            book.start = None
            book.end = None
            book.user_id = None
        return redirect(url_for('profile.user_profile', id=current_user.id))

    return render_template(
        "pages/user.html",
        user=user,
        blogs=blogs,
        books=books,
        shares=shares,
        current_id=current_user.id,
        date=date
    )


@profile.route('/<int:id>/edit/', methods=['GET', 'POST'])
def edit(id):
    """
    编辑个人页
    """
    date = datetime.date.today().strftime('%Y%m%d')[:4]
    user = User.query.filter_by(id=id).first()
    form = EditForm()
    if form.validate_on_submit():

        # must fill in
        user.username = form.username.data
        user.avatar_url = form.avatar_url.data
        user.info = form.info.data

        user.email = form.email.data
        user.birthday = form.birthday.data
        user.hometown = form.hometown.data
        user.group = form.group.data
        user.timejoin = form.timejoin.data
        user.timeleft = form.timeleft.data
        user.left = form.left.data

        # social networks' urls
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
    form.email.data = user.email
    form.birthday.data = user.birthday
    form.hometown.data = user.hometown
    form.group.data = user.group
    form.timejoin.data = user.timejoin
    form.timeleft.data = user.timeleft
    form.left.data = user.left

    form.personal_blog.data = user.personal_blog
    form.github.data = user.github
    form.flickr.data = user.flickr
    form.weibo.data = user.weibo
    form.zhihu.data = user.zhihu

    return render_template('/pages/edit.html', form=form, date=date)
