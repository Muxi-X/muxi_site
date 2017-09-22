#coding: utf-8
import functools 
import json 

from functools import wraps
from flask import abort , g , jsonify , request , current_app , make_response , abort 
from muxiwebsite.models import Permission , User

def permission_required(permission) :
    def decorator(f) :
        @wraps(f)
        def decorated(*args,**kwargs):
            if not g.current_user.can(permission) :
                abort(403)
            return f(*args,**kwargs)
        return decorated
    return decorator 

def login_required(f) :
    @wraps(f)
    def decorated(*args,**kwargs) :
        token = request.headers.get('token')
        if User.verify_auth_token(token) is not None :
            g.current_user = User.verify_auth_token(token)
            return f(*args,**kwargs)
        return jsonify({ }) , 401
    return decorated

def version_required(f) :
    @wraps(f)
    def decorated(*args,**kwargs) :
        secret_key = request.headers.get('secret_key')
        if secret_key is not None :
            if secret_key == current_app.config['KEY_FOR_VERSION'] : 
                return f(*args,**kwargs)
            return jsonify({ }) , 401
        return jsonify({ }) , 401
    return decorated


def tojson(f):
    """
    :function: tojson
    :args:
        - f: 被修饰的函数
    :rv: f()
    将视图函数的返回值转化成json的形式
    """
    @functools.wraps(f)
    def decorator(*args, **kwargs):
        rv = f(*args, **kwargs)
        status_or_headers = None
        headers = None
        if isinstance(rv, tuple):
            rv, status_or_headers, headers = rv + (None, ) * (3 - len(rv))
        if isinstance(status_or_headers, (dict, list)):
            headers, status_or_headers = status_or_headers, None

        rv = json.dumps(rv, indent=1, ensure_ascii=False)
        rv = make_response(rv)
        if status_or_headers is not None:
            rv.status_code = status_or_headers
        if headers is not None:
            rv.headers.extend(headers)
        return rv
    return decorator

