from uuid import uuid4

# from app import db
import datetime
import time


import json
from flask import Flask, jsonify, request
from neomodel import  BooleanProperty, IntegerProperty, StringProperty, StructuredNode, StructuredRel, RelationshipTo, RelationshipFrom, DateTimeProperty, JSONProperty, ArrayProperty, UniqueIdProperty
                      
from app.utils.kafka_producer import send_to_stream
from .base_criteria import BaseCriteria

# Task=1
class BaseTask(StructuredNode):
    # __primarykey__="Task_id"  
    Task_id =  UniqueIdProperty
    journey_id = StringProperty(unique_index=True)
    task_version =StringProperty(unique_index=True)
    created_on = DateTimeProperty()
    updated_on = DateTimeProperty()
    task_type = StringProperty()
    task_params = JSONProperty()
    meta_data = JSONProperty()
    unlock_criteria = RelationshipFrom(
        "BaseTask", "UNLOCK_CRITERIA", model=BaseCriteria)

    

    def run(self, *args, **kwargs):
        """
        Wrapper over Execute
        """
        try:
            dt = datetime.datetime.now().timestamp()
            result = self.execute(*args, **kwargs)
            de = datetime.datetime.now().timestamp()
            send_to_stream("RUN_TASK_EXECUTE", {
                'event_time': dt,
                'execution_data': result,
                'execute_time': dt-de,
            })
            return result
        except Exception as e:
            send_to_stream(
                "ERROR_TASK_EXECUTE", {'stack_trace': e})
    
    def execute(self, *args, **kwargs):
        pass
        """
        
        Function to override and execute
        """
        
        

    @classmethod
    def createNode(cls, **kwargs):
        task = cls()
        task.Task_id = uuid4()
        task.journey_id = kwargs.get('journey_id', uuid4())
        task.created_on = datetime.datetime.now()
        task.updated_on = datetime.datetime.now()
        task.unlock_criteria = kwargs.get("unlock_criteria", {
            'criteria': 'eq',
            'params': {
                'left': 1,
                'right': 1
            },
            'right': 'a'
        })
        if kwargs.get('meta'):
            task.meta = kwargs.get('meta', {})
        task.save()
        return task

    @classmethod
    def updateNode(cls, **kwargs):
        task = cls.nodes.get(id=kwargs.get("Task_id"))
        task.updated_on = datetime.datetime.now()
        if kwargs.get('meta'):
            task.meta = kwargs.get('meta', {})
        task.save()
        return task
    @classmethod
    def deleteNode(cls,**kwargs):
        task=cls.nodes.get(Task_id=kwargs.get("Task_id"))
        task.delete()
        return None 
        
    @classmethod
    def replaceNode(cls,**kwargs):
        task_to_replace=cls.nodes.get(Task_id=kwargs.get("id_1"))
        task_to_replace_with=cls.nodes.get(Task_id=kwargs.get("id_2"))
        t2=task_to_replace_with
        task_to_replace.delete()
        t2.Task_id=kwargs.get("id_1")
        t2.save()
        task_to_replace_with.delete()
        return t2
        
