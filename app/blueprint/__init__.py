from app import app
from app.task_executor.urls import task_executor_blueprint
from app.task_crud.urls import task_crud_blueprint
from app.utility_views.urls import util_views_blueprint

default_url_prefix = '/'


app.register_blueprint(task_executor_blueprint)
app.register_blueprint(task_crud_blueprint)
app.register_blueprint(util_views_blueprint)
