# coding: utf-8

"""
    wsgi.py

"""

from manage import app


if __name__ == "__main__":
    app.run(host="115.28.152.113", port=8000)
