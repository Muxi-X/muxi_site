import os
from . import shares
from .. import app
import json
from flask import Flask, request, send_from_directory,render_template , current_app , jsonify
import time
UPLOAD_FOLDER= '/root' + '/avatar_for_muxisite/'
ALLOWED_EXTENSIONS=set(['png','jpg','jpeg'])

def checkfloder():
    if os.path.isdir(UPLOAD_FOLDER):
        pass
    else:
        os.mkdir(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.split('.',1)[1] in ALLOWED_EXTENSIONS

@shares.route('/api/v2.0/upload/',methods = ['GET','POST'])
def upload_picture():
    if request.method == 'POST':
        checkfloder()
        file = request.files['file']
        li = [str(int(time.time())),file.filename.split('.',1)[1]]
        uploadtime ='.'.join(li)
        if file and allowed_file(file.filename):
            file.save(os.path.join(UPLOAD_FOLDER,uploadtime))
            url = os.path.join('/pictures/',uploadtime)
            return jsonify({ "filename" : url })
        return render_template('error415.html')
    return render_template('upload.html')

@shares.route('/pictures/<filename>/')
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER,filename)

