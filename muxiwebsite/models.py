# coding: utf-8

"""
    models.py
    ~~~~~~~~~

        数据库文件

                 图书数据库列表
                                                        books

                 id                         Integer, primary_key                           主键
                 url                        String url                                     对应豆瓣API的get url
                 name                       String                                         书名
                 summary                    String(编码) resp['summary']返回值             概要，豆瓣API获取
                 image                      String(编码) resp['image']返回值 url           封面图，API获取
                 user_id                    Integer，ForeignKey 外键 与users表的id相关联   与借阅者关联
                 end                        String,                                        书籍到期时间
                 status                     Boolean,                                       书籍的借阅状态，如果为True则被借阅
                ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                 用户数据库列表
                                                        users

                 id                         Integer, primary_key                           主键
                 username                   String                                         用户名
                 password                   password_hash                                  密码散列值
                 book                       relationship                                   借阅的书籍
                 comment                    relationship                                   发表的评论
                 share                      relationship                                   发布的分享
                 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                 分享数据库列表
                                                        shares

                 id                         Integer, primary_key                           主键
                 title                      String                                         分享的标题
                 share                      String                                         分享的内容
                                                                (采用markdown编辑器，数据库中存储的是markdown代码，前端进行html渲染)
                 author_id                  Integer, ForeignKey                            外键，分享的作者
                 comment                    relationship                                   分享对应的评论
                 timestamp                  datetime                                       时间戳
                 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                 评论数据库列表

                                                        comments
                 id                         Integer, primary_key                           主键
                 comment                    String                                         评论的内容，这里就是一般的纯文本
                 timestamp                  datetime                                       时间戳
                 share_id                   Integer, ForeignKey                            对应的分享的id
                 author_id                  Integer, ForeignKey                            对应的作者的id
                 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                 用户角色数据库列表

                                                        roles
                 id                         Integer, primary_key                           主键
                 name                       String                                         用户角色的名称
                 default                    Boolean                                        用户角色是否是默认值
                 permissions                Integer(base 16)                               用户角色对应的权限
                 users                      relationship                                   拥有该角色的用户列表
                 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                                                         blogs
                 id                         Integer, primary_key                           主键
                 body                       Text                                           博客的内容
                 body_html                  Text                                           博客内容的html格式
                 timestamp                  datetime                                       时间戳
                 author.id                  Integer, ForeignKey                            博客对应作者的id
                 comments                   relationship                                   该博客下的评论                            

"""

from . import db, login_manager, app
from flask import current_app
from flask.ext.login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import sys


# python 3搜索的不兼容
if sys.version_info[0] == 3:
    enable_search = False
else:
    enable_search = True
    import flask.ext.whooshalchemy as whooshalchemy


class Permission:
    """
    用户权限定义(base 16)
    """
    COMMENT = 0x02  # 评论权限
    WRITE_ARTICLES = 0x04  # 写文章权限
    MODERATE_COMMENTS = 0x08  # 修改评论权限
    ADMINISTER = 0x80  # 管理员权限，修改所有


class Role(db.Model):
    """
    用户角色定义
    """
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    users = db.relationship('User', backref='role', lazy='dynamic')

    @staticmethod
    def insert_roles():
        """
        插入角色
            1.User: 可以评论、写文章 true(默认)
            2.Moderator: 可以评论写文章,删除评论
            3.Administer: 管理员(想干什么干什么)
        需调用此方法，创建角色
        """
        roles = {
            # | 表示按位或操作,base 16进行运算
            'User': (Permission.COMMENT |
                     Permission.WRITE_ARTICLES, True),
            'Moderator': (Permission.COMMENT |
                          Permission.WRITE_ARTICLES |
                          Permission.MODERATE_COMMENTS, False),
            'Administrator': (0xff, False)
        }
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.permissions = roles[r][0]
            role.default = roles[r][1]
            db.session.add(role)  # 添加进数据库
        db.session.commit()  # 提交

    def __repr__(self):
        """该类的'官方'表示方法"""
        return '<Role %r>' % self.name


class Book(db.Model):
    """图书类"""
    __searchable__ = ['name', 'tag', 'summary']
    __tablename__ = "books"
    id = db.Column(db.Integer, primary_key = True)
    url = db.Column(db.String(164))
    name = db.Column(db.Text)
    author = db.Column(db.Text)
    tag = db.Column(db.String(164))
    summary = db.Column(db.Text)
    image = db.Column(db.String(164))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    status = db.Column(db.Boolean)
    start = db.Column(db.String(164))
    end = db.Column(db.String(164))

    def __repr__(self):
        return "%r :The instance of class Book" % self.name


class User(db.Model, UserMixin):
    """用户类"""
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(164))
    password_hash = db.Column(db.String(164))
    # avatar = db.String
    book = db.relationship('Book', backref="user", lazy="dynamic")
    share = db.relationship('Share', backref="user", lazy="dynamic")
    comments = db.relationship('Comment', backref='author', lazy='dynamic')
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    blogs = db.relationship('Blog', backref='author', lazy='dynamic')

    def __init__(self, **kwargs):
        """用户角色实现"""
        # 超类构造器(简化参数调用,不受Column的限制)
        super(User, self).__init__(**kwargs)
        if self.role is None:
            if self.username == current_app.config['MUXI_ADMIN']:
                self.role = Role.query.filter_by(permissions=0xff).first()
            if self.role is None:
                self.role = Role.query.filter_by(default=True).first()

    @login_manager.user_loader
    def load_user(user_id):
        """flask-login要求实现的用户加载回调函数
           依据用户的unicode字符串的id加载用户"""
        return User.query.get(int(user_id))

    @property
    def password(self):
        """将密码方法设为User类的属性"""
        raise AttributeError('密码原始值保密, 无法保存!')

    @password.setter
    def password(self, password):
        """设置密码散列值"""
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """验证密码散列值"""
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return "%r :The instance of class User" % self.username


if enable_search:
    whooshalchemy.whoosh_index(app, Book)


class Share(db.Model):
    """分享类"""
    __tablename__ = "shares"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text)
    share = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    comment = db.relationship('Comment', backref='share', lazy='dynamic')

    @staticmethod
    def generate_fake(count=10):
        # 生成虚拟数据
        from random import seed, randint
        import forgery_py

        seed()
        user_count = User.query.count()
        for i in range(count):
            u = User.query.offset(randint(0, user_count - 1)).first()
            p = Share(
                title=forgery_py.lorem_ipsum.title(randint(1, 5)),
                share=forgery_py.lorem_ipsum.sentences(randint(1, 5)),
                timestamp=forgery_py.date.date(True),
                author_id=u.id
            )
            db.session.add(p)
            db.session.commit()

    def __repr__(self):
        return "%r is instance of class Share" % self.title


class Comment(db.Model):
    """评论类"""
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    share_id = db.Column(db.Integer, db.ForeignKey('shares.id'))
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    blog_id = db.Column(db.Integer, db.Foreignkey('blogs.id'))

    """
    @staticmethod
    def generate_fake(count=10):
        # 生成虚拟数据
        from random import seed, randint
        import forgery_py

        seed()
        user_count = User.query.count()
        for i in range(count):
            u = User.query.offset(randint(0, user_count - 1)).first()
            c = Comment(
                comment=forgery_py.lorem_ipsum.sentences(randint(1, 5)),
                timestamp=forgery_py.date.date(True),
                author_id=u.id
            )
            db.session.add(c)
            db.session.commit()
        """

    def __repr__(self):
        return "<the instance of model Comment>"

class Blog(db.Model):
    """博客类"""
    __tablename__ = 'blogs'
    id = db.Column(db.Integer, primary_key = True)
    body = db.Column(db.Text)
    body_html = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=true, default=datetime.utnow)
    author.id = db.Column(db.Integer, db.Foreignkey('users.id'))
    comments = db.relationship('Comment', backref='blog', lazy='dynamic')

    @staticmethod
    def generate_fake(count=100):
        # 生成虚拟数据
        from random import randint
        import forgery_py

        seed()
        user_count = User.query.count()
        for i in range(count):
            u = User.query.offset(randint(0, user_count - 1)).first()
            b = Blog(body = forgery_py.lorem_ipsum.sentences(randint(1, 5)),
                timestamp =forgery_py.date.date(True)),
                author = u)
            db.session.add(b)
            db.session.commit()

    @staticmethod
    def on_changed_body(target, value, oldvalue, initiator):
        allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code',
                        'em', 'i', 'li', 'ol', 'pre', 'strong', 'ul',
                        'h1', 'h2', 'h3', 'p']
        target.body_html = bleach.linkify(bleach.clean(
            markdown(value, output_format='html'),
            tags=allowed_tags, strip=True))

    def to_json(self):
        #编写json字典
        json_post = {
            'url': url_for('api.get_blog', id=self.id, _external=True),
            #url部分因为还不知道视图函数名 先编了一个
            'body': self.body,
            'body_html': self.body_html,
            'timestamp': self.timestamp,
            'author': url_for('api.get_user', id=self.author_id,
                              _external=True),
            'comments': url_for('api.get_blog_comments', id=self.id,
                                _external=True),
            'comment_count': self.comments.count()
        }
        return json_blog

    @staticmethod
    def from_json(json_post):
        #该函数可以修改json字典的内容
        body = json_blog.get('body')
        if body is None or body == '':
            raise ValidationError('post does not have a body')
        return Blog(body=body)


db.event.listen(Blog.body, 'set', Blog.on_changed_body)
#用于监听markdown编辑器
