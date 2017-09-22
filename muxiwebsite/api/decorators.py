#coding: utf-8
from functools import wraps
from flask import abort , g , jsonify , request , current_app  
from muxiwebsite.models import Permission , User

def permission_required(permission) :
    def decorator(f) :
        @wraps(f)
        def decorated(*args,**kwargs):
            if not g.current_user.can(permission) :
                print g.current_user.role
                abort(403)
            return f(*args,**kwargs)
        return decorated
    return decorator

def login_required(f) :
    @wraps(f)
    def decorated(*args,**kwargs) :
        token = request.headers.get('token')
        if token is not None :
            g.current_user = User.verify_auth_token(token)
            return f(*args,**kwargs)
        return jsonify({"msg" : "login first!"}) , 401
    return decorated


def version_required(f) :
    @wraps(f)
    def decorated(*args,**kwargs) :
        secret_key = request.headers.get('secret_key')
        if secret_key is not None :
            if secret_key == current_app.config['KEY_FOR_VERSION'] : 
                return f(*args,**kwargs)
            return jsonify({"msg":"wrong key!"}) , 401
        return jsonify({"msg":"login first!"}) , 401
    return decorated



