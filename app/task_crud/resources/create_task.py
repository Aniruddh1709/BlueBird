from flask import request
from flask_restful import reqparse
from app.models import EmailTask,BaseTask
import datetime
from flask.views import MethodView
import json


class CreateTaskView(MethodView):
    

    # parser = reqparse.RequestParser()
    # parser.add_argument('name')


    #logic for this view is yet to be written
    def post(self):
        # id_=json.loads(request.data)
        c=EmailTask.createNode(Task_id='123')
        return "result"
    

        
        
        
        
        
       
        
      





      






    