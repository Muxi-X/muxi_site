# coding: utf-8

"""
	decorators.py
	~~~~~~~~~~~~~

		装饰器文件 
                没有用它!
"""

from functools import wraps
from flask import abort
from flask import g ,request , jsonify 
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

def login_required(f) :
    @wraps(f)
    def decorated(*args,**kwargs) :
        token_header = request.headers.get('token',None)
        if token_header :
            token_hash = token_header[6:]
            decode_token = base64.b64decode(token_hash)
            token = decode_token[:-1]
            g.current_user = User.verify_auth_token(token)
            return f(*arg,**kwargs)
        else :
            return jsonify ({'message' : '401 unAuthorization' }) , 401 
    return decorated

