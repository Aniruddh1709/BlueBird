from flask.views import MethodView

from flask import request, jsonify

from flask_restful import Resource

from app.api.error import HTTPBadRequest


class BaseResourcesView(Resource):
    def dispatch_request(self, *args, **kwargs):
        test_func = getattr(self, 'test_%s' % request.method.lower(), None)
        if test_func and not test_func(*args, **kwargs):
            raise HTTPBadRequest(message=(getattr(self, 'error', '')))
        data = super(BaseResourcesView, self).dispatch_request(*args, **kwargs)
        return jsonify({'data': data})


class BaseMethodView(MethodView):
    def validate_required_keys(self):
        method = request.method.lower()
        keys = getattr(self, 'required_keys_%s' % method, [])
        for key in keys:
            is_present = request.args.get(key) if method == 'get' else request.json.get(key)
            if not is_present:
                raise HTTPBadRequest(key + ' key is missing')
        return True

    def dispatch_request(self, *args, **kwargs):
        self.validate_required_keys()
        test_func = getattr(self, 'test_%s' % request.method.lower(), None)
        if test_func and not test_func(*args, **kwargs):
            raise HTTPBadRequest(message=(getattr(self, 'error', '')))
        data = super().dispatch_request(*args, **kwargs)
        return jsonify(
            dict(
                data=data,
            )
        )

    @classmethod
    def get_documentation(cls):
        documentation = DOC_MAP.get("Documentation" + cls.__name__, Documentation)
        request_methods = ['get', 'post', 'patch', 'put', 'head', 'options', 'delete']
        apiParamsMap = {}
        for method in request_methods:
            req_parser = getattr(cls, method + '_request_parser', None)
            if not req_parser:
                continue
            apiParams = []
            for arg in req_parser.args:
                apiParams.append({
                    "key": str(arg.name),
                    "description": str(arg.help),
                    "required": arg.required,
                    "type": str(arg.type)
                })
            apiParamsMap[method] = {
                "apiParam": apiParams,
                "apiParamExample": documentation.apiParamExample.get(method, documentation.apiParamExample),
                "apiSuccessExample": documentation.apiSuccessExample.get(method, documentation.apiSuccessExample),
                "apiHeaderExample": documentation.apiHeaderExample.get(method, documentation.apiHeaderExample)
            }

        return apiParamsMap
