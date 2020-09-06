import logging
from app.utils.env_variables import *

SERVICE_ACCESS_KEY = get_env_value('SERVICE_ACCESS_KEY')

APP_NAME = '<app_name>'
LOGGER_NAME = APP_NAME
LOGGING_LEVEL = logging.INFO

DEBUG = True
TESTING = False


HOST_SERVER_URL = '0.0.0.0'
HOST_SERVER_PORT = 80

# AWS Secrets
AWS_S3_SECRET_ACCESS_KEY = get_env_value('AWS_SECRET_ACCESS_KEY')
AWS_S3_ACCESS_KEY_ID = get_env_value('AWS_ACCESS_KEY_ID')
AWS_REGION = 'ap-southeast-1'
