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

    管理模块:
        backend:  木犀统一管理后台

    ~我们在路上，
        前方不会太远~。
"""

from flask import Flask, Markup, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import flask_login as login
from flask_login import LoginManager
from flask_pagedown import PageDown
from basedir import basedir
import flask_admin as admin
from flask_admin import Admin, BaseView, expose
from flask_admin.contrib.sqla import ModelView
import markdown
import os

# the root path of xueer
# __filename__ 就是占位
muxi_root_path = os.path.abspath(os.path.dirname("__filename__"))


# 实例创建＋蓝图注册
app = Flask(__name__)
# 配置(通用)
app.config['SECRET_KEY'] = "I hate flask!"
# app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + os.path.join(basedir, 'muxi_data.sqlite')  # 系统相应替换
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:1234@47.88.193.105/muxidb"
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['WHOOSH_BASE'] = "search.db"
app.config['MAX_SEARCH_RESULTS'] = 5  # 图书搜索最多加载5个搜索结果
app.config['MUXI_ADMIN'] = 'neo1218'
app.config["SHARE_PER_PAGE"] = 5
app.config["MUXI_SHARES_PER_PAGE"] = 10
app.config["SHARE_HOT_PER_PAGE"] = 3
app.config['MUXI_USERS_PER_PAGE'] = 10
app.config['BLOG_PER_PAGE'] = 10
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SERVER_NAME'] = 'muxistudio.com'


# 初始化扩展(app全局属性)
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'
pagedown = PageDown(app)

# @app.route('/')
# def index():
#     return "index"

# from . import views

class MyAdminIndexView(admin.AdminIndexView):
    """rewrite is_authenticated method"""
    def is_accessible(self):
        # return login.current_user.is_authenticated
        return login.current_user.is_admin()

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('auth.login'))


admin = Admin(
        app, name="木muxi犀", template_mode="bootstrap3",
        index_view=MyAdminIndexView(),
        base_template='my_master.html'
        )


from .models import User, Share, Blog, Book, Comment
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Book, db.session))
admin.add_view(ModelView(Share, db.session))
admin.add_view(ModelView(Comment, db.session))
admin.add_view(ModelView(Blog, db.session))


# jinja2 filters
@app.template_filter('neomarkdown')
def neomarkdown(markdown_content):
    """
    jinja2 markdown filter
    :param markdown_content: markdown
    :return: text
    """
    content = Markup(markdown.markdown(markdown_content))
    return content


# 蓝图注册
from .book import books
app.register_blueprint(books)

from .muxi import muxi
app.register_blueprint(muxi, url_prefix='/')

from .share import shares
app.register_blueprint(shares)

from .auth import auth
app.register_blueprint(auth, url_prefix='/auth')

from .blog import blogs
app.register_blueprint(blogs)

from profile import profile
app.register_blueprint(profile)

from api import api
app.register_blueprint(api, url_prefix="/api")

