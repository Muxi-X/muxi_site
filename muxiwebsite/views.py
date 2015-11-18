# coding: utf-8

"""
	views.py
	~~~~~~~~

		views for flask-admin
"""

from flask.ext.admin.contrib  import sqla
from flask.ext.admin import helpers, expose
from flask_admin import BaseView
import flask.ext.admin as admin
import flask.ext.login as login
from .auth.forms import LoginForm
from flask import redirect, url_for


# class MyModelView(sqla.ModelView):
# 	"""rewrite is_authenticated method"""
# 	def is_accessible(self):
# 		return login.current_user.is_admin()



# class MyAdminIndexView(admin.AdminIndexView):
# 
# 	@expose('/login', methods=('GET', 'POST'))
# 	def login_view(self):
# 		# handle user login
# 		form = LoginForm()
# 		if helpers.validate_form_on_submit(form):
# 			user = form.get_user()
# 			login.login_user(user)
# 
# 		if login.current_user.is_authenticated():
# 			return redirect(url_for('.index'))
# 		self._template_args['form'] = form
# 		return super(MyAdminIndexView, self).index()
# 
# 	@expose('/logout')
# 	def logout_view(self):
# 		form = LoginForm()
# 		login.logout_user()
# 		self._template_args['form'] = form
# 		return redirect(url_for('.index'))
