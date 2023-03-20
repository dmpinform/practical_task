from dataclasses import dataclass

import requests
from flask import redirect, request, session, url_for

from oauth2.application import services


@dataclass
class AuthPoint:
    auth_service: services.Authorization

    def login(self):
        return redirect(self.auth_service.get_auth_link())

    def callback_auth_code(self):
        code = request.args.get('code')
        state = request.args.get('state')

        if state == self.auth_service.get_request_state():
            user_cred = self.auth_service.get_user_cred(code)
            session['access_token'] = user_cred.access_token
            return redirect(url_for('get_start_api'))

        return 'Error authorization'

    def get_start_api(self):
        response = requests.get(
            url=self.auth_service.start_api,
            headers=self._get_header_auth(),
        )
        return response.json()

    @staticmethod
    def _get_header_auth():
        token = session.get('access_token', None)
        return {'Authorization': 'Bearer {}'.format(token)}
