import requests
from flask import redirect, request, session, url_for

from oauth2.application import services
from oauth2.constants import API_USERINFO


class AuthPoint:

    def __init__(self, auth_service: services.Authorization):
        self.auth_service: services.Authorization = auth_service

    def login(self):
        return redirect(self.auth_service.get_auth_link())

    def callback_auth_code(self):
        code = request.args.get('code')
        state = request.args.get('state')

        if state == self.auth_service.get_request_state():
            user_cred = self.auth_service.get_user_cred(code)
            session['access_token'] = user_cred.access_token
            return redirect(url_for('get_user_profile'))

        return 'Error authorization'

    def get_user_profile(self):
        response = requests.get(
            url=API_USERINFO,
            headers=self._get_header_auth(),
        )
        return response.json()

    @staticmethod
    def _get_header_auth():
        token = session['access_token']
        return {'Authorization': 'Bearer {}'.format(token)}
