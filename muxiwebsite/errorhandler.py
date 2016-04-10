from flask import request

@app.errorhandler(404)
def page_not_found(error):
    return 'Error 404 not found'
