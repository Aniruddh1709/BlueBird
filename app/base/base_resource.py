from flask import request, jsonify
from flask_restful import Resource
from app.api.error import HTTPBadRequest


class BaseResourcesView(Resource):
    
    def dispatch_request(self, *args, **kwargs):
        
        test_func = getattr(self, 'test_%s' % request.method.lower(), None)
        
        if test_func and not test_func(*args, **kwargs):
            
            raise HTTPBadRequest(message=(getattr(self, 'error', '')))
        data = super(BaseResourcesView, self).dispatch_request(*args, **kwargs)
        return jsonify({'data': data})
        