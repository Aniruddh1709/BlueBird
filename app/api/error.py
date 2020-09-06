from flask import jsonify

from weapp import app


class BaseAPIException(Exception):
    
    
    def __init__(self, message=None, status_code=None, payload=None):
        
        
        Exception.__init__(self)
        
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        
        
        rv = dict(self.payload or ())
        
        rv['message'] = self.message if self.message else ''
        
        return rv


class HTTPNotFound(BaseAPIException):
    
    
    status_code = 404


class HTTPMethodNotAllowed(BaseAPIException):
    
    status_code = 405


class HTTPForbidden(BaseAPIException):
    
    status_code = 403
    


class HTTPBadRequest(BaseAPIException):
    status_code = 400


@app.errorhandler(BaseAPIException)
def handle_invalid_usage(error):
    
    response = jsonify(error.to_dict())
    
    response.status_code = error.status_code
    return response
