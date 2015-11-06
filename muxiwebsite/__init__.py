# coding: utf-8
"""
    muxiwebsite: 木犀团队的官网
    ~~~~~~~~~~~~~~~~~~~~~~~~~

    木犀团队是华中师范大学自由的学生互联网团队，分为

        web(前端、后台)，设计， 安卓 组

    木犀官网是木犀团队的官方网站:
    功能模块:

        1.muxi:   木犀官网   木犀的简介信息
        2.blog:   木犀博客   木犀团队的博客
        3.book:   木犀图书   木犀图书管理
        4.share:  木犀分享   木犀内部的分享小站

    我们在路上，
        前方不会太远。
"""

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask.ext.pagedown import PageDown
from flask.ext.misaka import Misaka
import os
from basedir import basedir


# 实例创建＋蓝图注册
app = Flask(__name__)
# 配置(通用)
app.config['SECRET_KEY'] = "I hate flask!"
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + os.path.join(basedir, 'muxi_data.sqlite')  # 系统相应替换
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['WHOOSH_BASE'] = "search.db"
app.config['MAX_SEARCH_RESULTS'] = 5  # 图书搜索最多加载5个搜索结果
# app.config['UPLOAD_FOLDER'] = '/Users/apple/www/bitbucket/muxi_site/muxiwebsite/book/static/image/'
app.config['MUXI_ADMIN'] = 'neo1218'
app.config["SHARE_PER_PAGE"] = 5


# 初始化扩展(app全局属性)
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'
pagedown = PageDown(app)
misaka = Misaka(app)


# 蓝图注册
from .book import book
app.register_blueprint(book, url_prefix='/book')

from .muxi import muxi
app.register_blueprint(muxi, url_prefix='/muxi')

from .share import share
app.register_blueprint(share, url_prefix='/share')

from .auth import auth
app.register_blueprint(auth, url_prefix='/auth')
