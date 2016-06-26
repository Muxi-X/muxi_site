# coding: utf-8

"""
    views.py
    ~~~~~~~~

        木犀图书视图函数
        url                                        func
        /book                             主页 ; 显示:1.最近录入(6条)， 2.最近借阅
        /book/logout                      登出
        /bookin                           录入新书(只有管理员可见)
        /search                           站内搜索（支持两种模式）
        /search_results                   搜索结果页(提供借阅表单) 关于借阅状态
        /admin                            后台管理（只有管理员可见)
        /rter                             注册接口 (只有管理员可见)
        /<current_user>                   个人信息页(最近借阅)(快要到期 3天)
                      已过期的图书会flash消息提示
                           有情怀的flash提示
"""

from . import books
from .. import db, app
# from ..auth._decorate import auth_login
from werkzeug import secure_filename
from muxiwebsite.models import User, Book
from forms import BookForm, GetForm, LoginForm, RterForm
from flask import render_template, redirect, url_for, flash, request, session
from flask.ext.login import login_user, logout_user, login_required, current_user
from urllib2 import urlopen
import json
import datetime
import os

"""
                           ｜
              /------------/\-------------\
            /                              \
           |          木犀团队棒棒嗒         |
"""
# ------------------------------------------------------
#         """  我们在路上    前方不会太远 """
# ------------------------------------------------------


# 允许上传的文件扩展名
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])


def allowed_file(filename):
    """检查文件扩展名函数"""
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


# 对所有访客可见
@books.route('/', methods=["POST", "GET"])
# @auth_login(redirect_url='user')
def home():
    """
    首页视图函数

        1. 最近录入
        2. 最近借阅

        new_book_list: 最近录入新书列表(默认为6本, 依据时间[id]排序)
    """
    form = LoginForm()
    new_book_list = Book.query.order_by('-id').all()[:9]
    get_book_list = Book.query.filter_by(status=True).order_by('start desc').all()[:2]

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user)
            return redirect(url_for('books.home', id=current_user.id))
        flash('用户名或密码错误!')
    range_book_count = range(len(new_book_list)/6 + 1)

    return render_template('/pages/home.html', new_book_list=new_book_list,
                           get_book_list=get_book_list, form=form,
                           range_book_count=range_book_count)


# 对所有访客可见
@books.route('/search/', methods=["POST", "GET"])
def search():
    """
    搜索视图函数

        1. 搜索表单
        2. 显示搜索结果列表(最多加载5条搜索结果)

        搜索模式：
            1. 书名搜索（书名必须正确）
            2. 类别搜索（返回类别的图书：后台、前端、设计、互联网、其他）
    """
    if request.methos == 'POST':
        """前端 input 标签 action 实现重定向
           递交 search_results 处理"""
        pass


# 对所有访客可见
@books.route('/search_results/')
def search_results():
    """
    搜索结果页

        提供书籍借阅表单
    """
    search = request.args.get('search').lower()
    page = int(request.args.get('page') or 1)
    book_all = Book.query.all()
    book_search = {}
    book_result = []
    get_book_list = []

    for book in book_all:
        book.search = (str(book.name) + str(book.bid) + str(book.tag) + str(book.author)).lower()
        if search in book.search:
            book_result.append(book)

    last_page = (len(book_result)-1)/app.config['MAX_SEARCH_RESULTS']+1

    for each_book in book_result[(page-1)*app.config['MAX_SEARCH_RESULTS']:(page*app.config['MAX_SEARCH_RESULTS'])]:
        get_book_list.append(each_book)

    return render_template('/pages/search_results.html',
        get_book_list=get_book_list, page=page, last_page=last_page,
        search=search
        )


# 对所有访客可见，但只有登录用户可以借阅(html改动)
@books.route('/info/<int:id>/', methods=["POST", "GET"])
def info(id):
    form = GetForm()
    book = Book.query.get_or_404(id)
    if form.validate_on_submit():
        formday = str(form.day.data)
        day = formday[0:4] + formday[5:7] + formday[8:10]
        start = str(datetime.date.today().strftime('%Y%m%d'))
        dminuss = int(day)-int(start)
        if dminuss >= 0:
            book.start = start
            book.user_id = current_user.id
            book.status = True  # 已被借
            book.end = day
            return redirect(url_for('profile.user_profile', id=current_user.id))
        else:
            flash('光阴似箭、岁月如梭,时间－你不能篡改她，更不能逆转她!')
            return redirect(url_for('books.info', id=id))
    return render_template('/pages/info.html', book=book, form=form)


# 只对管理员可见
@books.route('/bookin/', methods=["POST", "GET"])
@login_required
def bookin():
    """
    书籍录入

        输入书籍的名字，将书籍的

            书名， 封面， 简介 录入数据库
    """
    if current_user.role_id == 2:
        form = BookForm()

        if form.validate_on_submit():
            bookname = form.bookname.data
            get_url = "https://api.douban.com/v2/book/search?q=%s" % bookname
            resp_1 = json.loads(urlopen(get_url).read().decode('utf-8'))
            book_id = resp_1['books'][0]['id']
            url = "https://api.douban.com/v2/book/%s" % book_id
            resp_2 = json.loads(urlopen(url).read().decode('utf-8'))
            book = Book(url=url, name=resp_2['title'], author=resp_2['author'][0], \
                        tag=form.tag.data, summary=resp_2['summary'], \
                        image=resp_2['images'].get('large'), user_id=None, end=None, \
                        status=False)
            db.session.add(book)
            db.session.commit()
            flash('书籍已录入！')
            return redirect(url_for('books.bookin'))
        return render_template('/pages/bookin.html', form=form)
    else:
        return redirect(url_for('books.home'))


# 对所有登录用户可见
@books.route('/logout/')
@login_required
def logout():
    """退出视图函数"""
    logout_user()
    return redirect(url_for('home'))
