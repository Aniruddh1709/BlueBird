from flask import url_for
from flask_admin.contrib.sqla import ModelView, form
from flask_admin.model.form import converts
from wtforms import fields, validators

from authhandler import AuthServiceHandler
from flask import request, redirect
from app.utils import HTTP_STATUS_OK
from app import app


class IsStaffMixin(object):
    def test_func(self):
        token = request.cookies.get('access_token', None)
        if not token:
            app.logger.info('access token not found in cookies')
            return False
        response = AuthServiceHandler.validate_access_token(token)
        if not response:
            app.logger.info('No response from auth service')
            return False
        if response.status_code != HTTP_STATUS_OK:
            app.logger.info('invalid access token ' + str(response.status_code))
            return False
        return True

    def get_redirect_url(self):
        raise NotImplementedError()

    def has_permission(self):
        return self.test_func()

    def handle_no_permission(self):
        return redirect(self.get_redirect_url())


class BaseModelFormConvertor(form.AdminModelConverter):

    @converts('sqlalchemy_utils.types.uuid.UUIDType')  # includes UnicodeText
    def conv_my_uuid(self, field_args, **extra):
        field_args.setdefault('label', u'UUID')
        field_args['validators'].append(validators.UUID())
        return fields.StringField(**field_args)


class BaseModelView(IsStaffMixin, ModelView):
    create_modal = True
    edit_modal = True
    can_delete = False
    page_size = 10
    can_edit = False
    can_view_details = True
    column_default_sort = None
    column_list = []
    column_formatters = dict(state=lambda v, c, m, p: m.state.value)
    ignore_hidden = False
    column_filters = []
    model_form_converter = BaseModelFormConvertor

    def get_count_query(self):
        """
            Prevents count(*) query, over-ride this if count needed.
        """    
        return None

    def get_redirect_url(self):
        return url_for('google-login')

    def is_accessible(self):
        return super().has_permission()

    def inaccessible_callback(self, name, **kwargs):
        return super().handle_no_permission()
