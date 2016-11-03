FROM python:2.7
MAINTAINER Muxi Studio

ENV DEPLOY_PATH /muxiwebsite

RUN mkdir -p $DEPLOY_PATH
WORKDIR $DEPLOY_PATH

RUN apt-get update
RUN apt-get install gunicorn -yq
Add requirements.txt requirements.txt
RUN pip install --index-url http://pypi.doubanio.com/simple/ -r requirements.txt --trusted-host=pypi.doubanio.com
# RUN pip install --index-url https://pypi.python.org/simple/ -r requirements.txt --trusted-host=pypi.python.org

Add . .
