import os
from flask import Flask
from app.request_wrapper import Request
from flask_restful import Api
from app import settings
from neomodel import config
from app.utils.env_variables import get_env_value





class BaseApi(Api):
    def add_resource(self, resource, *urls, **kwargs):
        
        
        kwargs['strict_slashes'] = False
        
        if self.app is not None:
            
            self._register_view(self.app, resource, *urls, **kwargs)
            
        else:
            
            self.resources.append((resource, urls, kwargs))
            

    def error_router(self, original_handler, e):
        pass
        
        
    #from app.exceptions.handler import error_handler
        
    #return error_handler(e, super(BaseApi, self).error_router, original_handler)
        


def create_app():
    
    app = Flask(__name__)
    app.config.from_object(settings)
    config.DATABASE_URL = 'bolt://neo4j:12345678@localhost:11008'
    config.ENCRYPTED_CONNECTION = False   
    
    
    env = get_env_value('ENV', 'development').lower()
    if env == 'testing':
        pass
    Request(app)
    
   
    app.name = app.config.get('APP_NAME')
    
    return app


app = create_app()



api = BaseApi(app)






#db = SQLAlchemy(app)
__import__('app.api')
__import__('app.blueprint')
__import__('app.utils')
__import__('app.models')


