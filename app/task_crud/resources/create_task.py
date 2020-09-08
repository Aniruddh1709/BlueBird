from flask import request
from flask_restful import reqparse
from app.models import EmailTask,BaseTask
import datetime
from flask.views import MethodView
import json


task_type_dict = {
    "email_task":"EmailTask",
    "base_task":"BaseTask",
    "CSV_upload":"CSVUploadTask"
}

class JourneyCrudView(MethodView):
    

    parser = reqparse.RequestParser()
    parser.add_argument('task_type',type=str,location='args',required=True)
    parser.add_argument('journey_id',type=str,location='args',required=True)
    parser.add_argument('rel_data',type=list,location='args')


    #logic for this view is yet to be written
    def post(self):
        args=JourneyCrudView.parser.parse_args()
        Node_created=task_type_dict.get(args.get('task_type')).createNode(journey_id=args.get('journey_id'),rel_data=args.get('rel_data'))
        return "node created"
    

        
        
        
        
        
       
        
      





      






    