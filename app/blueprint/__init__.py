from app import app
from app.task_executor.urls import task_executor_blueprint,create_blueprint,response_blueprint


default_url_prefix = '/tasks'


app.register_blueprint(task_executor_blueprint)
app.register_blueprint(create_blueprint)
app.register_blueprint(response_blueprint)
