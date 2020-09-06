from flask import Blueprint
from app import BaseApi

from .resources import TaskExecutorView

task_executor_blueprint = Blueprint(
    'task_executor', __name__, url_prefix='/task')

api = BaseApi(task_executor_blueprint)

api.add_resource(TaskExecutorView, '/execute')
