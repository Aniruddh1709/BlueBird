from flask import Blueprint

from app import BaseApi


from .resources import JourneyCrudView


task_crud_blueprint = Blueprint('task_crud', __name__, url_prefix='/journey')

api = BaseApi(task_crud_blueprint)


api.add_resource(JourneyCrudView, '/create')
