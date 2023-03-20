import os

from flask import Flask

from oauth2.adapters.api.controllers.auth import AuthPoint
from oauth2.application import services


class App(Flask):

    def __init__(self):
        super().__init__(__name__)
        self.secret_key = os.getenv('SESSION_SECRET_KEY')

    def add_auth_routes(self, auth_service: services.Authorization):
        auth_point = AuthPoint(auth_service=auth_service)

        self.add_url_rule(
            '/',
            view_func=auth_point.login,
        )

        self.add_url_rule(
            '/oauth2/callback/google',
            view_func=auth_point.callback_auth_code,
        )

        self.add_url_rule(
            '/oauth2/callback/vk',
            view_func=auth_point.callback_auth_code,
        )

        self.add_url_rule(
            '/start',
            view_func=auth_point.get_start_api,
        )
