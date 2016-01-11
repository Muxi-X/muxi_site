# coding: utf-8
"""
    views.py
    ~~~~~~~~

    木犀个人页视图

"""

from . import profile
from flask import render_template, url_for
from ..models import User


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

# @profile.route('/<int:id>/blogs/')
# def blogs(id):
#     user = User.query.get_or_404(id)
#     blogs = user.blogs
#     return render_template('components/list.html', blogs=blogs)
# 
# 
# @profile.route('/<int:id>/comments/')
# def comments(id):
#     pass
# 
# 
# @profile.route('/<int:id>/books/')
# def books(id):
#     pass
