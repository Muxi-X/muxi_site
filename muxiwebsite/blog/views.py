# coding: utf-8

from . import blogs
from flask import render_template, render_template_string, redirect, url_for, request, \
        current_app , g  , jsonify
from flask_login import current_user, login_required
from sqlalchemy import desc
from ..models import Blog, Comment, Tag, User, Type , Permission
from .forms import CommentForm
from muxiwebsite import db, auth
from ..decorators import login_required , permission_required
from ..login import Login
from ..signup import Signup
from werkzeug.security import generate_password_hash
import base64

@blogs.route('/')
def index():
    """
    木犀博客首页
    """
    page = int(request.args.get('page') or 1)
    article_tag = Tag.query.all()
    blog_all = Blog.query.order_by('-id').all()
    blog_list = Blog.query.order_by('-id').paginate(page, current_app.config['BLOG_PER_PAGE'], False)
    for blog in blog_all:
        blog.date = "%d/%02d/%02d" % (blog.timestamp.year, blog.timestamp.month, blog.timestamp.day)
        try:
            blog.avatar = User.query.filter_by(id=blog.author_id).first().avatar_url
        except AttributeError:
            blog.avatar = ""
        blog.content = blog.body
        blog.intro = blog.summary
    article_date = []

    for blog in blog_all:
        if blog.index not in article_date:
            article_date.append(blog.index)

    return render_template("pages/index.html", blog_list=blog_list,
                           article_tag=article_tag, article_date=article_date)


@blogs.route('/index/<string:index>/', methods=["GET"])
def ym(index):
    """
    博客归档页面
    :return:
    """
    blog_list = []
    for blog in Blog.query.all():
        if blog.index == index:
            blog_list.append(blog)
    for blog in blog_list:
        blog.date = "%d/%02d/%02d" % (blog.timestamp.year, blog.timestamp.month, blog.timestamp.day)
        blog.avatar = User.query.filter_by(id=blog.author_id).first().avatar_url
        blog.content = blog.body
    article_date = []
    for blog in Blog.query.all():
        if blog.index not in article_date:
            article_date.append(blog.index)
    return render_template('pages/archive.html', blog_list=blog_list,
            index=index, article_date=article_date)


@blogs.route('/post/<int:id>/', methods=["POST", "GET"])
def post(id):
    """
    博客文章页面
    """
    form = CommentForm()
    blog = Blog.query.get_or_404(id)
    blog.content = blog.body
    blog.date = "%d年%d月%d日 %d:%d" % (blog.timestamp.year,
            blog.timestamp.month, blog.timestamp.day, blog.timestamp.hour,
            blog.timestamp.minute)
    if form.validate_on_submit():
        # 提交评论
        if current_user.is_authenticated:
            name = current_user.username
            uid = current_user.id
        else:
            name = form.username.data
            uid = 0
        comment = Comment(
            comment=form.comments.data,
            author_id= uid,
            author_name = name,
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
        comment.date = str(comment.timestamp)[:-10]
        comment.content = comment.comment
    return render_template("pages/post.html", blog=blog, form=form, comment_list=comment_list)


@blogs.route('/type/<string:type>/')
def types(type):
    """
    返回对应分类下的文章
    分类: WEB, 设计, 安卓, 产品, 关于
    """
    page = int(request.args.get('page') or 1)
    blog_all = Blog.query.all()
    type_item = Type.query.filter_by(value=type).first()
    blog_list = Blog.query.filter_by(type_id=type_item.id).paginate(page, current_app.config['BLOG_PER_PAGE'], False)
    for blog in blog_all:
        blog.date = "%d/%02d/%02d" % (blog.timestamp.year, blog.timestamp.month, blog.timestamp.day)
        blog.avatar = User.query.filter_by(id=blog.author_id).first().avatar_url
        blog.content = blog.body

    article_date = []
    for blog in blog_all:
        if blog.index not in article_date:
            article_date.append(blog.index)

    return render_template('pages/type.html', blog_list=blog_list, type=type,
            article_date=article_date)



tags = ['frontend','backend','android','design','product']

@blogs.route('/api/v2.0/',methods=['GET'])
def get_blogs2() :
    """
    获取所有博客
    """
    page = request.args.get('page',1,type=int)
    blog_list = Blog.query.order_by('id').paginate(page,current_app.config['BLOG_PER_PAGE'],False)
    pages_count = len(Blog.query.all())/current_app.config['BLOG_PER_PAGE'] + 1
    if page > pages_count :
        return jsonify({}) , 404
    blogs_count = len(Blog.query.all())

    return jsonify({
        'blogs' : [ blog.to_json()  for blog in blog_list.items ] ,
        'count' : blogs_count ,
        'page'  : page ,
        'pages_count' : pages_count ,
        }) , 200

@blogs.route('/api/v2.0/sort/',methods=['GET'])
def index_blogs2() :
    """
    博客首页,根据所选的标签显现博客
    """
    page = request.args.get('page',1,type=int)
    sort = request.args.get('sort')
    item = Blog.query.filter_by(type_id=sort)
    blog_list = item.order_by('id').paginate(page,current_app.config['BLOG_PER_PAGE'],False)
    pages_count = blog_list.total/current_app.config['BLOG_PER_PAGE'] + 1
    if page > pages_count :
        return jsonify({
            "message" : "can not find the page"
            }) , 404
    blogs = blog_list.items
    return jsonify({
        "pages_count" : pages_count ,
        "page" : page ,
        "blogs" : [blog.to_json() for blog in blogs ]
        }), 200

@blogs.route('/api/v2.0/send/',methods=['POST'])
@login_required
def add_blog2() :
    """
    登录用户发博客
    """
    blog = Blog()
    blog.title = request.get_json().get("title")
    blog.body = request.get_json().get("body")
    blog.img_url = request.get_json().get("img_url")
    blog.summary = request.get_json().get("summary")
    blog.type_id = request.get_json().get("type_id")
    blog.author_id = g.current_user.id
    db.session.add(blog)
    db.session.commit()
    return jsonify({
            "id" : blog.id ,
            "author_id" : blog.author_id
        }) , 200

@blogs.route('/api/v2.0/<int:id>/delete/',methods=['DELETE'])
@login_required
@permission_required(Permission.WRITE_ARTICLES)
def deleted2(id) :
    """
    删除博客
    """
    blog = Blog.query.get_or_404(id)
    db.session.delete(blog)
    db.session.commit()
    return jsonify({
        "delete" : blog.id ,
        }) , 200

@blogs.route('/api/v2.0/<int:id>/add_comment/',methods=['POST'])
@login_required
def comment2(id) :
    """
    发送评论
    """
    comment = Comment()
    comment.comment = request.get_json().get("comment")
    comment.blog_id = id
    comment.author_id = g.current_user.id

    db.session.add(comment)
    db.session.commit()

    return jsonify({
        "message" : " added a  comment!"
        }) , 200


@blogs.route('/api/v2.0/<int:id>/comment/',methods=['GET'])
def view_comment2(id) :
    """
    查看评论
    """
    comments= Comment.query.filter_by(blog_id=id).all()
    return jsonify({
        'comments' : [ comment.to_json() for comment in comments ] ,
        })  , 200


@blogs.route('/api/v2.0/<int:id>/views/',methods=['GET'])
def view2(id) :
    """
    查看单个博客和他的评论
    """
    blog = Blog.query.get_or_404(id)
    comments= Comment.query.filter_by(blog_id=id).all()
    return jsonify({
        'comments' : [ comment.to_json() for comment in comments ] ,
        'blog' : blog.to_json()
        })  , 200

@blogs.route('/api/v2.0/login/',methods=['POST'])
def login_for_blog() :
    email  = request.get_json().get("email")
    pwd = request.get_json().get("password")
    l = Login(email,pwd)
    res = l.login()
    return jsonify ({
        'token' : res[0]
        }) , res[1]

@blogs.route('/api/v2.0/signup/',methods=['POST'])
def signup_for_blog() :
    un = request.get_json().get("username")
    email = request.get_json().get("email")
    password = request.get_json().get("password")
    s = Signup(un,email,password)
    res =  s.signup()
    return jsonify ({
        'created' : res[0]
        }) , res[1]


