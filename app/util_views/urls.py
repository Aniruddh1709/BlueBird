from flask import Blueprint
from app import BaseApi

from app.util_views.resources import SendgridResponseView

util_views_blueprint = Blueprint('util_views', __name__, url_prefix='utils/')

api = BaseApi(util_views_blueprint)


api.add_resource(SendgridResponseView, '/sendgrid')
