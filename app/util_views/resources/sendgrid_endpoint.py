from flask import request, jsonify, render_template
from flask.views import MethodView
from flask_restful import reqparse
import json
from neomodel import BooleanProperty, StructuredNode
from app.models import EmailTask, BaseTask
from flask.views import MethodView

# this endpoint receives the data from the webhook and uses it to call the next task


class SendgridResponseView(MethodView):

    """
    Retrieval of Responses to an Activity is handled here
    """
    parser = reqparse.RequestParser()
    parser.add_argument('data', type=json, location='json')

    def post(self):
        # TODO: USE Request Parser
        result = json.loads(request.data)
        args = result[0]
        event_opened = args['event']
        return "result has been received"
