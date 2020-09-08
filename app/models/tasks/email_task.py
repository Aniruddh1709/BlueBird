import json
from uuid import uuid4
import datetime
import time
from flask import Flask, jsonify, request, render_template


from neomodel import  BooleanProperty, IntegerProperty, StringProperty, StructuredNode, StructuredRel, RelationshipTo, RelationshipFrom, DateTimeProperty, JSONProperty,ArrayProperty, UniqueIdProperty,config
                      
from app.utils.kafka_producer import send_to_stream
from app.models.base.base_criteria import BaseCriteria
from app.models.base.base_task import BaseTask

import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


# StatesDict = {
#     'opened':lambda open : True if(open) else False,
#     'sent':lambda sent : True if(sent) else False,
#     'clicked':lambda clicked : True if(clicked) else False,
#     'replied':lambda replied : True if(replied) else False,
#     'delivered':lambda open : True if(delivered) else False
# }

class EmailTask(BaseTask):
    
    EMAIL_SENT=RelationshipTo('BaseTask','Email_Sent',model=BaseCriteria)
    EMAIL_OPENED=RelationshipTo('BaseTask','Email_Opened',model=BaseCriteria)
    EMAIL_FAILED=RelationshipTo('BaseTask','Email_Failed',model=BaseCriteria)

    
    
    @classmethod
    def execute(self,**kwargs):
        mail_id=kwargs.get("mail_id")
        emailed_to=self.nodes.get(Task_id=kwargs.get("Task_id")) 
        # emailed_to.task_params=kwargs.get("task_parameters")
        email_attributes=emailed_to.task_params
        message = Mail(
        from_email='',
        to_emails=mail_id,
        subject='Sending with Twilio SendGrid is Fun',
        html_content=render_template('EMAIL TXT.txt',emailattributes=email_attributes)) #template can be added here using render template
        try:
            sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
            response = sg.send(message)
            print(response.status_code)
            print(response.body)
            print(response.headers)
        except Exception as e:
            print(e.message)
                       
        return "email sent" #return statement only for reference to check working of code

    
    def mail_response(self,**kwargs):
        event=kwargs.get('event') 
        current_node=self.nodes.get(Task_id=kwargs.get('current_node_id'))
        if(event=='open'):
            current_node.on_open(current_node=current_node,next_node_id=kwargs.get('next_node_id'))
        elif(event=='fail'):
            current_node.on_fail(current_node=current_node,next_node_id=kwargs.get('next_node_id'))
        elif(event=='sent'):
            current_node.on_send(current_node=current_node,next_node_id=kwargs.get('next_node_id'))
              
    
    def on_send(self,**kwargs):
        current_node=kwargs.get('current_node')
        next_node=current_node.EMAIL_SENT.get(Task_id=kwargs.get('next_node_id'))
        next_node.execute(**kwargs)
    def on_fail(self,**kwargs):
        current_node=kwargs.get('current_node')
        next_node=current_node.EMAIL_FAILED.get(Task_id=kwargs.get('next_node_id'))
        next_node.execute(**kwargs)
    def on_open(self,**kwargs):
        current_node=kwargs.get('current_node')
        next_node=current_node.EMAIL_OPENED.get(Task_id=kwargs.get('next_node_id'))
        next_node.execute(**kwargs)
   
    @classmethod
    def createNode(cls,**kwargs):
        # task=super.createNode(journey_id=kwargs.get('journey_id'))
        # commented out the initialization code because of a confusion i faced with calling the parent class create and child class create

        rel_data=kwargs.get('rel_data')
        


        

        

     
        

            
        
        
        
        
    




    