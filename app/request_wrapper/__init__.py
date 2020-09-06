import datetime
import uuid
import requests as base_requests
from flask import g, current_app, request, Response
from logging import Logger
class Request(object):
    def __init__(self, app=None, logging=True):
        self.app = app
        if app is not None:
            app.before_request(self.allow_incoming_request)
            app.before_request(self.capture_incoming_request)
            if logging:
                Logger(app)
    def allow_incoming_request(self):
        if self.app.config.get('ALLOW_REQUESTS_WITHOUT_SERVICE_KEY'):
            return 
        allowed_url_path = ['/admin', '/healthcheck', '/google','/email','/','/tasks','/inboundresponse','/task/','/createnode']
        allowed_url_path += self.app.config.get('ALLOWED_PATHS_WITHOUT_SERVICE_KEY', [])
        for path in allowed_url_path:
            if path in request.path:
                return
        if self.app.config.get('SERVICE_ACCESS_KEY') != self._get_from_header('SERVICE-ACCESS-KEY'):
            return Response(
                {'message': 'cannot access service'},
                status=403,
                mimetype='application/json'
            )
    @staticmethod
    def _get_from_header(key):
        headers = request.headers
        return headers.get(key, '')
    @staticmethod
    def get_service_access_key():
        return current_app.config.get('SERVICE_ACCESS_KEY')
    @classmethod
    def _request_id(cls):
        request_id = g.get('request_id')
        if request_id:
            return request_id
        request_id = cls._get_from_header('X-Request-Id') or str(uuid.uuid1())
        g.request_id = request_id
        return request_id
    @classmethod
    def _request_source_start_time(cls):
        request_source_start_time = cls._get_from_header('X-Request-Source-Time')
        if request_source_start_time:
            g.request_source_start_time = request_source_start_time
            return request_source_start_time
        request_source_start_time = str(datetime.datetime.now().timestamp())
        g.request_source_start_time = request_source_start_time
        return request_source_start_time
    @classmethod
    def _source_app(cls):
        source_app = g.get('source_app')
        if source_app:
            return source_app
        source_app = cls._get_from_header('X-Source-App') or current_app.name
        g.source_app = source_app
        return source_app
    @classmethod
    def _sequence_number(cls):
        sequence_number = g.get('sequence_number')
        if sequence_number:
            return sequence_number
        sequence_number = cls._get_from_header('X-Sequence-Number')
        if sequence_number:
            sequence_number = sequence_number + '.' + current_app.name
        else:
            sequence_number = current_app.name
        g.sequence_number = sequence_number
        return sequence_number
    @classmethod
    def _request_start_time(cls):
        request_start_time = g.get('request_start_time')
        if request_start_time:
            return request_start_time
        request_start_time = datetime.datetime.now()
        g.request_start_time = request_start_time
        return request_start_time
    @classmethod
    def capture_incoming_request(cls):
        cls._request_start_time()
        cls._request_id()
        cls._source_app()
        cls._sequence_number()
        cls._request_source_start_time()
    @classmethod
    def _request_header(cls, kwargs):
        headers = kwargs.get('headers', {})
        try:
            request_id = cls._request_id()
            sequence_number = cls._sequence_number()
            source_app = cls._source_app()
            service_access_key = cls.get_service_access_key()
        except RuntimeError:
            # it means working outside of app and request context.
            return kwargs
        headers.update({
            'X-Request-Id': request_id,
            'X-Sequence-Number': sequence_number,
            'X-Source-App': source_app,
            'SERVICE-ACCESS-KEY': service_access_key,
            'X-Request-Source-Time': str(datetime.datetime.now().timestamp())
        })
        kwargs.update({
            'headers': headers
        })
        return kwargs
    @classmethod
    def request(cls, method, url, **kwargs):
        kwargs = cls._request_header(kwargs)
        return base_requests.request(method, url, **kwargs)
    @classmethod
    def get(cls, url, params=None, **kwargs):
        kwargs = cls._request_header(kwargs)
        return base_requests.get(url, params=params, **kwargs)
    @classmethod
    def options(cls, url, **kwargs):
        kwargs = cls._request_header(kwargs)
        return base_requests.options(url, **kwargs)
    @classmethod
    def head(cls, url, **kwargs):
        kwargs = cls._request_header(kwargs)
        return base_requests.head(url, **kwargs)
    @classmethod
    def post(cls, url, data=None, json=None, **kwargs):
        kwargs = cls._request_header(kwargs)
        return base_requests.post(url, data=data, json=json, **kwargs)
    @classmethod
    def put(cls, url, data=None, **kwargs):
        kwargs = cls._request_header(kwargs)
        return base_requests.put(url, data=data, **kwargs)
    @classmethod
    def patch(cls, url, data=None, **kwargs):
        kwargs = cls._request_header(kwargs)
        return base_requests.patch(url, data=data, **kwargs)
    @classmethod
    def delete(cls, url, **kwargs):
        kwargs = cls._request_header(kwargs)
        return base_requests.delete(url, **kwargs)