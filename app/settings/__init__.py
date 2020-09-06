from app.utils.env_variables import get_env_value

env = get_env_value('ENV', 'development').lower()

if env == "production":
    from .production import *
elif env == "testing":
    from .testing import *
elif env == "staging":
    from .staging import *
else:
    from .local import *


# POSTGRES = ServiceConfigManager.get_postgres_config(APP_NAME)
# POSTGRES = {
#     'user':'',
#     'pw':'',
#     'host':'127.0.0.1',
#     'port':'5432',
#     'db':'testdb'
# }

# SQLALCHEMY_DATABASE_URI = 'postgresql://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES
# SQLALCHEMY_BINDS = {
#     'tasks':        'neo4j://localhost/users',
#     'appmeta':      'sqlite:////path/to/appmeta.db'
# }