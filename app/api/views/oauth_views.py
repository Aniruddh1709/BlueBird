import json
from flask import (
    make_response, redirect, render_template,
    url_for, request
)
from flask_restful import Resource, reqparse

from .authhandler import AuthServiceHandler

from app import app
from app.utils import HTTP_STATUS_OK


class GoogleLogin(Resource):
    def get(self):
        headers = {
            'Content-Type': 'text/html'
        }
        return make_response(render_template('login.html'), HTTP_STATUS_OK, headers)


class GoogleLoginSubmit(Resource):
    def get(self):
        return redirect(
            AuthServiceHandler.get_google_login_url(
                callback_url=app.config['GOOGLE_CALLBACK_URL']
            )
        )


class GoogleLoginCallback(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('code', type=str)
        args = parser.parse_args()
        if not args.get('code', None):
            app.logger.info('no code provided in callback url')
            return redirect(url_for('google-login'))

        response = AuthServiceHandler.google_callback(
            app_code=args['code'],
            user_callback_url=app.config['GOOGLE_CALLBACK_URL']
        )
        if response.status_code != HTTP_STATUS_OK:
            app.logger.info('error while getting access token from auth service - ' + str(response.status_code))
            return redirect(url_for('google-login'))
        data = json.loads(response.text)
        access_token = data.get('data', {}).get('access_token', '')
        if not access_token:
            app.logger.info('invalid access token received from auth service')
            return redirect(url_for('google-login'))
        response = AuthServiceHandler.validate_access_token(access_token)
        if not response:
            app.logger.info('No response from auth service')
            return redirect(url_for('google-login'))
        if response.status_code != HTTP_STATUS_OK:
            app.logger.info('invalid access token ' + str(response.status_code))
            return redirect(url_for('google-login'))

        resp = make_response(redirect(url_for('admin.index')))
        resp.set_cookie('access_token', access_token)
        return resp


class GoogleLogout(Resource):
    def get(self):
        token = request.cookies.get('access_token', None)
        AuthServiceHandler.google_logout(
            access_token=token
        )
        resp = make_response(redirect(url_for('google-login')))
        resp.set_cookie('access_token', '', expires=0)
        return resp
