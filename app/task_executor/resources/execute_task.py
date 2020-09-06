from flask import request, jsonify, render_template
from flask.views import MethodView
from flask_restful import reqparse
import json
from app.models import EmailTask, BaseTask
from neomodel import BooleanProperty, StructuredNode
from flask.views import MethodView


class TaskExecutorView(MethodView):

    """
    Retrieval of Responses to an Activity is handled here
    """
    parser = reqparse.RequestParser()
    # parser.add_argument('task_paramters',type=list,location='json')
    parser.add_argument('Task_id')
    parser.add_argument('email_id')

    def patch(self):
        args = TaskExecutorView.parser.parse_args()
        Task_id = args['Task_id']
        # task_parameters=args['task_parameters']
        email_id = args['email_id']
        result = EmailTask.execute(Task_id, email_id)

        return result
