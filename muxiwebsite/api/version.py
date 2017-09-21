# coding: utf-8
from muxiwebsite import rds  
from . import api
from ..decorators import version_required , tojson  
from flask import jsonify, request 
import ast

"""
    version.py
    ~~~~~~~~~~
    木犀内外app版本api 
""" 

@api.route('/app/',methods=['GET']) 
@version_required
@tojson
def get_app() : 
    """
    获取木犀内外app版本信息
    """
    if not rds.get('apps'):
        rds.set('apps', "[{'name':'muxisite','version':'none','download_url':'none','v_name':'none'}]") 
        rds.save()
    apps = rds.get('apps')
    return ast.literal_eval(apps)     
    

@api.route('/app/',methods=['POST'])
@version_required
def update_app() : 
    """
    更新木犀内外app版本信息 
    """ 
    if not rds.get('apps'):
        rds.set('apps', "[{'name':'muxisite','version':'none','download_url':'none','v_name':'none'}]") 
    version = request.get_json().get('version')
    url = request.get_json().get('url')
    name = request.get_json().get('name')
    app_data = {
            "v_name" : name, 
            "version" : version, 
            "download_url" : url, 
    }
    apps = ast.literal_eval(rds.get('apps'))
    apps.append(app_data) 
    rds.set('apps', str(apps)) 
    rds.save() 
    return jsonify({'msg': 'add new version data'}), 201

@api.route('/app/latest/',methods=['GET'])
@version_required
@tojson
def latest_app() : 
    """
    返回木犀内外app的最后一个版本信息 
    """ 
    if not rds.get('apps'):
        rds.set('apps', "[]")
    apps = rds.get("apps")
    return ast.literal_eval(apps)[-1]
