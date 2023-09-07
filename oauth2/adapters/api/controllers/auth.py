from dataclasses import dataclass

import jwt
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
        if self.auth_service.is_valid_state(state):
            user_cred = self.auth_service.get_user_cred(code)
            session['access_token'] = user_cred.access_token
            session['id_token'] = user_cred.id_token
            return redirect(url_for('get_start_api'))

        return 'Error authorization: not valid state'

    def get_start_api(self):
        response = requests.get(
            url=self.auth_service.get_start_api(),
            headers=self._get_header_auth(),
        )
        return response.json()

    @staticmethod
    def get_payload_id_token():
        id_token = session['id_token']
        return jwt.decode(id_token, options={'verify_signature': False})

    @staticmethod
    def _get_header_auth():
        access_token = session.get('access_token', None)
        return {'Authorization': 'Bearer {}'.format(access_token)}
