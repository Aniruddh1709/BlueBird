from app import app
from flask_admin import Admin, AdminIndexView


admin = Admin(
    app,
    index_view=AdminIndexView(name='Home', url='/<app_name>/admin'),
    template_mode='bootstrap3',
    base_template='base_admin.html'
)
