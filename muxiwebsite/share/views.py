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
from .forms import ShareForm, CommentForm, EditForm
from .. import  db, app
from ..models import Share, Comment, User, Permission
# from ..auth._decorate import auth_login, auth_logout
from flask import url_for, render_template, redirect, request, current_app
from flask.ext.login import current_user, login_required
from ..decorators import permission_required
from sqlalchemy import desc
from sqlalchemy import func


@shares.route('/')
def index():
	"""
	muxi_share 分享你的知识

	主页，默认显示最新的分享
	添加分页，默认显示第一页
	"""

	flag = 0
	# 添加分页, share变为分页对象
	page = int(request.args.get('page'))
	shares_count = {}
	if request.args.get('sort') == None:
		shares_pages = Share.query.order_by('-id').paginate(page, app.config['SHARE_PER_PAGE'], False)
		shares = shares_pages.items
	elif request.args.get('sort') == "new":
		flag = 0
		shares_pages = Share.query.order_by('-id').paginate(page, app.config['SHARE_PER_PAGE'], False)
		shares = shares_pages.items
	elif request.args.get('sort') == "hot":
		flag = 1
		shares = []
		# shares = Share.query.join(Share.comment).order_by(Comment.count)[:15]
		for share in Share.query.all():
			shares_count[share] = share.comment.count()
		shares_count = sorted(shares_count.items(), lambda x, y: cmp(y[1], x[1]))
		for share_tuple in shares_count:
			shares.append(share_tuple[0])
		shares = shares[:5]
		# shares_pages = shares.paginate(page, app.config["SHARE_PER_PAGE"], False)
		shares_pages = None

	for share in shares:
		share.content = share.share
		share.avatar = "http://7xj431.com1.z0.glb.clouddn.com/屏幕快照%202015-10-08%20下午10.28.04.png"
		share.comment_count = share.comment.count()
		share.author = User.query.filter_by(id=share.author_id).first().username
	return render_template('share_index.html', shares=shares, flag=flag, Permission=Permission, shares_pages=shares_pages)


@shares.route('/view/<int:id>/', methods=["GET", "POST"])
def view_share(id):
    """
    显示特定id的分享，相关信息以及评论
    实现评论表单发表自己的评论
    """
    share = Share.query.get_or_404(id)
    comments = Comment.query.filter_by(share_id=share.id).all()
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(
            comment = form.comment.data,
            author_id = current_user.id,
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

    # share.avatar = User.query.filter_by(share=share.id).first().avatar_hash
    share.avatar = "http://7xj431.com1.z0.glb.clouddn.com/屏幕快照%202015-10-08%20下午10.28.04.png"
    share.content = share.share
    share.comments = len(Comment.query.filter_by(share_id=share.id).all())

    for comment in comments:
        comment.avatar = "http://7xj431.com1.z0.glb.clouddn.com/download.jpeg"
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
    """分享"""
    form = ShareForm()
    if form.validate_on_submit():
        share = Share(
                title = form.title.data,
                share = form.share.data,
                author_id = current_user.id
                )
        db.session.add(share)
        db.session.commit()
        return redirect(url_for('.index', page = 1))

    return render_template("share_send.html", form=form)


@shares.route('/edit-share/<int:id>/', methods=["POST", "GET"])
@login_required
@permission_required(Permission.WRITE_ARTICLES)
def edit(id):
    """
    用户可以修改自己的分享
    """
    form = EditForm()
    share = Share.query.filter_by(id=id).first()
    if form.validate_on_submit():
        share.title = form.title.data
        share.share = form.share.data
        db.session.add(share)
        db.session.commit()
        return redirect(url_for("shares.index", page=1))
    form.title.data = share.title
    form.share.data = share.share
    return render_template(
            "edit-share.html",
            form=form
            )
