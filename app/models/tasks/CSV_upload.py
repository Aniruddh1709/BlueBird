import json
from uuid import uuid4
from flask import Flask, jsonify, request, render_template
from neomodel import  BooleanProperty, IntegerProperty, StringProperty, StructuredNode, StructuredRel, RelationshipTo, RelationshipFrom, DateTimeProperty, JSONProperty,ArrayProperty, UniqueIdProperty,config
from app.utils.kafka_producer import send_to_stream
from app.models.base.base_criteria import BaseCriteria
from app.models import BaseTask
from . import EmailTask
import pandas as pd




class CSVUploadTask(EmailTask):

    ON_UPLOAD_SUCCESS=RelationshipTo('BaseTask','Next_Task',model=BaseCriteria)
    ON_UPLOAD_FAILED=RelationshipTo('BaseTask','Next_Task',model=BaseCriteria)

    def execute(self,**kwargs):
        df=pd.read_csv('app\models\tasks\CSV File\Example data.csv')
        for i in df.index:
            mail_id=df['email'][i]
            Current_Task_Id=df['Task1_id'][i]
            Next_Task_Id=df['Task2_id'][i]
            Current_Task=EmailTask.nodes.get(Task_id=Current_Task_Id)
            Next_Task=EmailTask.nodes.get(Task_id=Next_Task_Id)
            Next_Task.execute(mail_id,Task_id=Next_Task_Id)

        return





