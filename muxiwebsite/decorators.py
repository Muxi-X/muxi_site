# coding: utf-8

"""
	decorators.py
	~~~~~~~~~~~~~

		装饰器文件
                没有用它!
"""

from functools import wraps
from flask import abort
from flask_login import current_user
from .models import Permission


# 权限判断装饰器
def permission_required(permission):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.can(permission):
                abort(403)
                return f(*args, **kwargs)
        return decorated_function
    return decorator
