# coding: utf-8

from . import i
from flask import render_template, redirect, url_for, request


@i.route('/')
def index():
    """
    木犀博客首页
    """
    return render_template("index.html")
