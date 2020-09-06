from flask import request,jsonify,render_template
from flask.views import MethodView
from flask_restful import reqparse
import json
from neomodel import BooleanProperty, StructuredNode
from app.models import EmailTask,BaseTask
from flask.views import MethodView

#this endpoint receives the data from the webhook and uses it to call the next task
class ResponsesView(MethodView):
    
    """
    Retrieval of Responses to an Activity is handled here
    """
    parser = reqparse.RequestParser()
    parser.add_argument('Data',type=list,location='json')

    def post(self):
        # args = ResponsesView.parser.parse_args()    
        # print(args)
        result=json.loads(request.data)
        args=result[0]
        event_opened=args['event']
        
            


        
       
        
        
        
        return "result has been received"  #return statement only for reference to check working of code
    

        
        
        
        
        
        
    