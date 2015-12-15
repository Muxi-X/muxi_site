# coding: utf-8

from . import blogs
from flask import render_template, render_template_string
from ..models import Blog
from .. import muxi_root_path
from jinja2 import FileSystemLoader


@blogs.route('/')
def index():
    """
    木犀博客首页
    blog_list: 博客文章的集合
    blog.img_url
    blog.name
    blog.date
    blog.like_number
    blog.comment_number
    for item in tag
    item.value
    blog.avatar
    """
    blog_list = Blog.query.all()
    for blog in blog_list:
        blog.img_url = "http://7xj431.com1.z0.glb.clouddn.com/1-140G2160520962.jpg"
        blog.name = "占位"
        blog.date = 1
        blog.like_number = 1
        blog.comment_number = 1
    # return render_template_string just like this name: return a string
    # return render_template("%s/muxiwebsite/blog/templates/pages/index.html" % muxi_root_path,
    #                             blog_list=blog_list)
    loader = FileSystemLoader('%s/muxiwebsite/blog/templates/pages/index.html' % muxi_root_path,
                           {'blog_list':blog_list})
    return loader
    # return render_template("pages.index.html")


@blogs.route('/post/<int:id>/')
def post(id):
    """
    博客文章页面
    """
    return render_template("pages/post.html")
