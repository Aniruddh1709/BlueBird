from app import api

from app.api.views import (
    GoogleLogin, GoogleLoginCallback,
    GoogleLoginSubmit, GoogleLogout
)

api.add_resource(GoogleLogin, '/<app_name>/google/login', endpoint='google-login')
api.add_resource(GoogleLoginSubmit, '/<app_name>/google/login/submit', endpoint='google-login-submit')
api.add_resource(GoogleLoginCallback, '/<app_name>/google/callback', endpoint='google-callback')
api.add_resource(GoogleLogout, '/<app_name>/google/logout', endpoint='google-logout')
