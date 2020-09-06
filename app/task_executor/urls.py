from flask import Blueprint

from app import BaseApi


from .resources.webhook_endpoint import ResponsesView
from .resources.execute_task import TaskExecutorView
from .resources.create_task import CreateTaskView


task_executor_blueprint = Blueprint('task_executor', __name__)
response_blueprint = Blueprint('response_view',__name__,url_prefix='/')
create_blueprint = Blueprint('createview',__name__)

api = BaseApi(task_executor_blueprint)
api2=BaseApi(response_blueprint)
api3=BaseApi(create_blueprint)



api.add_resource(TaskExecutorView, '/task/')
api2.add_resource(ResponsesView,'/')
api3.add_resource(CreateTaskView,'/createnode')


