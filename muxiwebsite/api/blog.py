# coding: utf-8
from . import blogs
from flask import render_template, render_template_string, redirect, url_for, request, \
        current_app
from flask_login import current_user, login_required
from sqlalchemy import desc
from ..models import Blog, Comment, Tag, User, Type
from .forms import CommentForm
from muxiwebsite import db, auth


tags = ['frontend', 'backend', 'android', 'design', 'product']

# 木犀博客首页
@api.route('/blog/',methods=['GET'])
def get_blog():
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

#    for blog in blog_all:
#        if blog.index not in article_date:
#            article_date.append(blog.index)

    return jsonify([{
                   'blog_tag':blog.tag.value,
                   'blog_date':"%d/%02d/%02d" % (blog.timestamp.year, blog.timestamp.month, blog.timestamp.day),
                   'blog_avatar':User.query.filter_by(id=blog.author_id).first().avatar_url,
                   'blog_body':blog.body}
                    for blog in blog_list]) , 200

#博客归档页面return:
@api.route('/blog/index/<string:index>/', methods=["GET"])
def ym(index):
    blog_list = []
    for blog in Blog.query.all():
        if blog.index == index:
            blog_list.append(blog)
        article_date = []
    for blog in Blog.query.all():
        if blog.index not in article_date:
            article_date.append(blog.index)
    return jsonify([{
                   'index':blog.index,
                   'blog_date': "%d/%02d/%02d" % (blog.timestamp.year, blog.timestamp.month, blog.timestamp.day),
                   'blog_avatar'=User.query.filter_by(id=blog.author_id).first().avatar_url,
                   'blog_content' = blog.body}
                    for blog in blog_list]) , 200


#博客文章页面
@api.route('/blog/post/<int:id>/', methods=["GET"])
def post(id):
    blog = Blog.query.get_or_404(id)
    comment_list =Comment.query.filter_by(blog_id=id).all()
    return jsonify({
                   'body':blog.body,
                   'author_id':blog.author_id,
                   'blog_id':blog.id,
                   'blog_date': "%d年%d月%d日 %d:%d" % (blog.timestamp.year,
                           blog.timestamp.month, blog.timestamp.day, blog.timestamp.hour,
                           blog.timestamp.minute),
                   'comment': [comment.to_json() for comment in comment_list ]}) , 200



@api.route('/blog/post/<int:id>/', methods=["POST"])
def comment(id):
    blog = Blog.query.get_or_404(id)
    # 提交评论
    comments = Comment.query.filter_by(blog_id=id).all()
    #if current_user.is_authenticated():
    #    name = current_user.username
    #    uid = current_user.id
    #else:
    #    name = request.get_json().get("name")
    #    uid = 0
    #comment = Comment()
    #comment.comment =request.get_json().get("comment")
    #comment.author_id= request.get_json().get("uid")
    #comment.author_name =  name
    comment.blog_id= request.get_json().get("id")




    if request.method == 'POST' :
        comment = Comment()
        comment.comment = request.get_json().get("comment")
        comment.blog_id = id 
        comment.author_id = request.get_json().get("author_id") 
     #   comment.auhtor_name = \
      #  User.query.filter_by(id=author_id).first().username

        db.session.add(comment)
        db.session.commit()
        return jsonify(comment.to_json()) , 201 
    
        blog.avatar = \
        User.query.filter_by(id=share.author_id).first().avator_url
    
    for comment in comments :
        comment.avatar = \
        User.query.filter_by(id=comment.author_id).first().avatar_url
        comment.username = \
        User.query.filter_by(id=comment.author_id).first().username
        comment.content  = comment.comment 


    blog.comment_number += 1
    db.session.add(blog)
    db.session.commit()
    return 200











#  返回对应分类下的文章,分类: WEB, 设计, 安卓, 产品, 关于
@api.route('/blog/type/<string:type>/',methods=['GET'])
def types(type):

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

    return jsonify([{
                    'blog_tag':blog.tag.value,
                    'blog_date':"%d/%02d/%02d" % (blog.timestamp.year, blog.timestamp.month, blog.timestamp.day),
                    'blog_avatar':Use3r.query.filter_by(id=blog.author_id).first().avatar_url,
                    'blog_body':blog.body

                    'type_item':type_item,
                    'page':page,}
                    for blog in blog_list]) , 200
