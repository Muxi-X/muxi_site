# coding: utf-8

"""
    urls.py
    ~~~~~~~

        处理url定向

"""

from urlparse import urlparse, urljoin
from flask import redirect, url_for, request

def is_safe_url(target):
    """is safe url ?"""
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
            ref_url.netloc == test_url.netloc

def get_redirect_target():
    """find rediect target url in next or refer"""
    for target in request.values.get('next'), request.referrer:
        if not target:
            continue
        if is_safe_url(target):
            return target

def redirect_back(endpoint, **values):
    # target = request.form['next']
    target = request.referrer
    return target
    if not target or not is_safe_url(target):
        target = url_for(endpoint, **values)
    return redirect(target)

