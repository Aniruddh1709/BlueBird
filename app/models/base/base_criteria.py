from uuid import uuid4

# from app import db
import datetime


import json
from flask import Flask, jsonify, request
from neomodel import  BooleanProperty, IntegerProperty, StringProperty, StructuredNode, StructuredRel, RelationshipTo, RelationshipFrom, DateTimeProperty, JSONProperty, ArrayProperty, UniqueIdProperty
from app.utils.kafka_producer import send_to_stream


def DEFAULT_FUNC(x):
    return True


# The Following can be defined as classes as well.
CriteriaDict = {
    'eq': lambda x, y: x == y,
    'gt': lambda x, y: x > y,
    'gte': lambda x, y: x >= y,
    'lt': lambda x, y: x < y,
    'lte': lambda x, y: x <= y,
}



class BaseCriteria(StructuredRel):
    
    criteria = StringProperty()
    params = JSONProperty()
    created_on = DateTimeProperty()
    updated_on = DateTimeProperty()

    @classmethod
    def check_criteria(cls, criteria_id):
        """
        Checks if Unlock Criteria is fulfilled
        """
        criteria = cls.nodes.get(criteria_id)
        result = CriteriaDict[criteria.criteria](criteria.parameters)
        return result

    @classmethod
    def create(cls, **kwargs):
        criteria = cls()
        criteria.id = uuid4()
        criteria.criteria = kwargs.get('criteria')
        criteria.params = kwargs.get('params')
        criteria.created_on = datetime.datetime.now()
        criteria.updated_on = datetime.datetime.now()
        if kwargs.get('meta'):
            criteria.meta = kwargs.get('meta', {})
        criteria.save()
        return criteria

    @classmethod
    def update(cls, **kwargs):
        criteria = cls.nodes.get(id=kwargs.get("id"))
        criteria.criteria = kwargs.get('criteria')
        criteria.params = kwargs.get('params')
        criteria.updated_on = datetime.datetime.now()
        if kwargs.get('meta'):
            criteria.meta = kwargs.get('meta', {})
        criteria.save()
        return criteria
