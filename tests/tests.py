#coding: utf-8
import unittest
from flask import current_app , url_for,jsonify
from muxiwebsite import create_app
from flask_sqlalchemy import SQLAlchemy
import random
from muxiwebsite.models import Share
import json
TOKEN = str(0)
SHARE_ID = 1
BLOG_ID = 1
db = SQLAlchemy()
number = random.randint(501,900)

class BasicTestCase(unittest.TestCase) :
    def setUp(self) :
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()
        db.create_all()

    def tearDown(self) :
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_app_exist(self) :
        self.assertFalse(current_app is None)

    def test_a_signup(self) :
        response = self.client.post(
                    url_for('api.signup',_external=True),
                    data = json.dumps({
                        "username" : str(number) ,
                        "email" : str(number) ,
                        "password" : str(number) }) ,
                    content_type = 'application/json')
        self.assertTrue( response.status_code == 200 )

    def test_b_login(self) :
        response = self.client.post(
                    url_for('api.login',_external=True),
                    data = json.dumps({
                        "password" : str(number) ,
                        "email" : str(number)
                        }) ,
                    content_type = 'application/json'
                    )
        s = json.loads(response.data)['token']
        global TOKEN
        TOKEN = s
        self.assertTrue( response.status_code == 200 )

    def test_get_shares(self) :
        response = self.client.get(
                    url_for('api.get_shares',_external=True),
                    content_type = 'application/json')
        self.assertTrue( response.status_code == 200 )

    def test_get_comment(self) :
        response = self.client.get(
                    url_for('api.view_share',id=SHARE_ID,_external=True),
                    content_type = 'application/json')
        self.assertTrue( response.status_code == 200  )

    def test_get_comment_and_share(self) :
        response = self.client.get(
                    url_for('api.views',id=SHARE_ID,_external=True),
                    content_type = 'application/json')
        self.assertTrue( response.status_code == 200 )

    def test_get_sorted(self) :
        response = self.client.get(
                    url_for('api.index',page=1,sort='frontend',_external=True),
                    content_type = 'application/json')
        self.assertTrue( response.status_code == 200 )

    def test_b_send_share(self) :
        response = self.client.post(
                    url_for('api.add_share',_external=True),
                    headers = {
                        "token": TOKEN ,
                        "Accept" : "application/json" ,
                        "Content_Type" :"application/json"
                        },
                    data = json.dumps({
                        "title" : "####" ,
                        "share" : "###" ,
                        "tags" : "frontend" }),
                    content_type = 'application/json'
                    )
        t = json.loads(response.data)['id']
        global SHARE_ID
        SHARE_ID = int(t)
        self.assertTrue( response.status_code == 200 )

    def test_c_send_comment(self) :
        response = self.client.post(
                url_for('api.add_comment',id=1,_external=True),
                headers = {
                    "token": TOKEN ,
                    "Accept" : "application/json" ,
                    "Content_Type" :"application/json"
                    },
                data = json.dumps(dict(comment="###")),
                content_type = 'application/json'
                    )
        self.assertTrue( response.status_code == 200 )

    def test_w_edit_share(self) :
        response = self.client.put(
                    url_for('api.edit',id=SHARE_ID,_external=True),
                    headers = {
                        "token": TOKEN ,
                        "Accept" : "application/json" ,
                        "Content_Type" :"application/json"
                        },
                    data = json.dumps({
                        "title" : "####" ,
                        "share" : "###" }) ,
                    content_type = 'application/json'
                    )
        self.assertTrue( response.status_code == 200 )

    def test_z_delete_share(self) :
        response = self.client.delete(
                    url_for('api.delete',id=SHARE_ID,_external=True),
                    headers = {
                        "token": TOKEN ,
                        "Accept" : "application/json" ,
                        "Content_Type" :"application/json"
                        },
                    content_type = 'application/json'
                    )
        print response.status_code
        self.assertTrue( response.status_code == 200 )

    def test_z_get_profile(self) :
        response = self.client.get(
                    url_for('api.show_profile',username = str(number),_external=True) ,
                    headers = {
                        "token" : TOKEN ,
                        "Content_Type" : "application/json"
                        } ,
                    content_type = 'application/json'
                    )
        self.assertTrue ( response.status_code == 200 )

    def test_z_edit_profile(self) :
        response = self.client.post(
                    url_for('api.edit_profile',username = str(number),_external=True) ,
                    headers = {
                        "token" : TOKEN ,
                        "Accpet" : "application/json" ,
                        "Content_Type" : "application/json"
                        } ,
                    data = json.dumps({
                        "info" : "2333" ,
                        }) ,
                    content_type = 'application/json' ,
                    )
        self.assertTrue( response.status_code == 201 )

    def test_zz_add_blog(self) :
        response = self.client.post(
                    url_for('api.add_blog',_external=True) ,
                    headers = {
                        "token" : TOKEN ,
                        "Accpet" : "application/json" ,
                        "Content_Type" : "application/json"
                        } ,
                     data = json.dumps({
                        "title" : "####" ,
                        "body" : "###" ,
                        "tpye" : "aa" ,
                        "img_url" : "dnfij" ,
                        "summary" : "bf"  ,
                        "tag" : "fbd" }) ,
                    content_type = 'application/json' ,
                    )
        t = json.loads(response.data)['id']
        global BLOG_ID
        BLOG_ID = int(t)
        self.assertTrue (response.status_code == 200 )

    def test_zz_send_comment(self) :
        response = self.client.post(
                    url_for('api.comment',id=BLOG_ID,_external=True),
                    headers = {
                        "token": TOKEN ,
                        "Accept" : "application/json" ,
                        "Content_Type" :"application/json"
                        },
                    data = json.dumps(dict(comment="###")),
                    content_type = 'application/json'
                    )
        self.assertTrue( response.status_code == 200 )

    def test_zz_s_get_comment(self) :
        response = self.client.get(
                    url_for('api.view_comment',id=BLOG_ID,_external=True),
                    content_type = 'application/json')
        self.assertTrue( response.status_code == 200  )

    def test_zz_s_get_comment_and_share(self) :
        response = self.client.get(
                    url_for('api.view',id=BLOG_ID,_external=True),
                    content_type = 'application/json')
        self.assertTrue( response.status_code == 200 )

    def test_zz_s_get_sorted_blogs(self) :
        response = self.client.get(
                    url_for('api.index_blogs',sort="aa",_external=True),
                    content_type = 'application/json')
        self.assertTrue( response.status_code == 200 )

    def test_zz_s_get_all_blogs(self) :
        response = self.client.get(
                    url_for('api.get_blogs',_external=True),
                    content_type = 'application/json')
        self.assertTrue( response.status_code == 200 )

    def test_zzz_delete_blog(self) :
        response = self.client.delete(
                    url_for('api.deleted',id=BLOG_ID,_external=True),
                    headers = {
                        "token": TOKEN ,
                        "Accept" : "application/json" ,
                        "Content_Type" :"application/json"
                        },
                    content_type = 'application/json'
                    )
        self.assertTrue( response.status_code == 200 )

