# conding: utf-8
from . import api
from muxiwebsite.models import User
from flask import jsonify, request
#from .authentication import auth
from muxiwebsite import db

@api.route('/login/', methods=['POST'])
def login():
    email = request.get_json().get("email")
    pwd = request.get_json().get("password")
    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({}), 403
    if user is not None and user.verify_password(pwd):
        token = user.generate_auth_token()
        return jsonify ({
            'token' : token
                                                                                    }),  200
    else:
        return jsonify({}), 502
