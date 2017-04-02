# coding: utf-8

"""
    views.py ~ 木犀分享视图文件

        主页: 发布分享

        /:  主页
        /share:  发布分享的页面
        /login:  登录页
        /logout: 登出页
        /new: 显示最新分享
        /hot: 显示最热分享
        /view_share: 查看分享的具体信息，评论，发表评论
"""

# models import
from . import shares
from jinja2 import Environment
from .forms import ShareForm, CommentForm, EditForm
from .. import  db, app
from ..models import Share, Comment, User, Permission
from flask import url_for, render_template, redirect, request, current_app, Markup
from flask_login import current_user, login_required
from ..decorators import permission_required
from sqlalchemy import desc
from sqlalchemy import func
import markdown


tags = ['frontend', 'backend', 'android', 'design', 'product']

@shares.route('/')
def index():
    
    muxi_share 分享你的知识
	主页，默认显示最新的分享
	添加分页，默认显示第一页
	

    flag = 0
    # 添加分页, share变为分页对象
    page = int(request.args.get('page') or 1)
    shares_count = {}
    # tags = ['frontend', 'backend', 'android', 'design', 'product']

    sort_arg = request.args.get('sort')
    if sort_arg == None:
        shares_pages = Share.query.order_by('-id').paginate(page, app.config['SHARE_PER_PAGE'], False)
        shares = shares_pages.items

    elif sort_arg == "new":
        flag = 0
        shares_pages = Share.query.order_by('-id').paginate(page, app.config['SHARE_PER_PAGE'], False)
        shares = shares_pages.items

    elif sort_arg == "hot":
        flag = 1
        shares = []
        for share in Share.query.all():
            shares_count[share] = share.comment.count()
        shares_count = sorted(shares_count.items(), lambda x, y: cmp(y[1], x[1]))
        for share_tuple in shares_count:
            shares.append(share_tuple[0])
        shares = shares[:5]
        shares_pages = None

    elif sort_arg in tags:
        flag = tags.index(sort_arg) + 2
        shares = []
        this_arg =  Share.query.filter_by(tag=sort_arg)
        shares_pages = this_arg.order_by('-id').paginate(page, app.config['SHARE_PER_PAGE'], False)
        shares = shares_pages.items


    for share in shares:
        share.avatar = User.query.filter_by(id=share.author_id).first().avatar_url
        share.comment_count = share.comment.count()
        share.author_id = share.author_id
        share.author = User.query.filter_by(id=share.author_id).first().username

    return render_template('share_index.html', tags = tags, shares=shares, flag=flag, Permission=Permission, shares_pages=shares_pages)


@shares.route('/view/<int:id>/', methods=["GET", "POST"])
def view_share(id):
    
    显示特定id的分享，相关信息以及评论
    实现评论表单发表自己的评论

    share = Share.query.get_or_404(id)
    share.author = User.query.filter_by(id=share.author_id).first().username
    comments = Comment.query.filter_by(share_id=share.id).all()
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(
            comment = form.comment.data,
            author_id = current_user.id,
            author_name = User.query.filter_by(id=current_user.id).first().username,
            share_id = id,
			count = 0
            )
        db.session.add(comment)
        db.session.commit()
        this_comment = Comment.query.filter_by(
			comment=form.comment.data,
			author_id=current_user.id,
			share_id = id,
			).first()
        this_comment.count += 1
       return redirect(url_for('shares.view_share', id=id))

    share.avatar =  User.query.filter_by(id=share.author_id).first().avatar_url
    share.comments = len(Comment.query.filter_by(share_id=share.id).all())

    for comment in comments:
        comment.avatar = User.query.filter_by(id=comment.author_id).first().avatar_url
        comment.username = User.query.filter_by(id=comment.author_id).first().username
        comment.content = comment.comment
    return render_template(
        'share_second.html',
        form = form,
        share = share,
        comments = comments
        )


@login_required
@shares.route('/send/', methods=["GET", "POST"])
def add_share():
    分享
    form = ShareForm()
    if form.validate_on_submit():
        share = Share(
                title = form.title.data,
                share = form.share.data,
                tag = form.tag.data,
                author_id = current_user.id
                )
        db.session.add(share)
        db.session.commit()
        return redirect(url_for('.index', page = 1))
    return render_template("share_send.html", form=form, tags = tags)


@login_required
@shares.route('/delete/<int:id>/', methods=["GET", "POST"])
@permission_required(Permission.WRITE_ARTICLES)
def delete(id):
    
    User could delete his share
    
    share = Share.query.filter_by(id=id).first()
    db.session.delete(share)
    db.session.commit()
    return redirect(url_for("shares.index"))



@shares.route('/edit-share/<int:id>/', methods=["POST", "GET"])
@login_required
@permission_required(Permission.WRITE_ARTICLES)
def edit(id):
    
    用户可以修改自己的分享
    
    form = EditForm()
    share = Share.query.filter_by(id=id).first()
    if form.validate_on_submit():
        share.title = form.title.data
        share.share = form.share.data
        share.tag = form.tag.data
        db.session.add(share)
        db.session.commit()
        return redirect(url_for("shares.index", page=1))
    form.title.data = share.title
    form.share.data = share.share
    form.tag.data = share.tag
    return render_template(
            "edit-share.html",
            form = form,
            tags = tags
            )


