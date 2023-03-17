import os

import requests
from flask import Flask, redirect, request, session, url_for
from flask_pydantic import validate

from oauth2.adapters.flow import AuthRequest, TokenRequest
from oauth2.adapters.google.settings import Credential
from oauth2.application import dto, services
from oauth2.constants import API_USERINFO, SCOPE_USERINFO_PROFILE

app = Flask(__name__)

credential = Credential()

app.secret_key = os.getenv('SESSION_SECRET_KEY')


class Flow:
    auth_request_params = dto.AuthRequestParams(
        client_id=credential.CLIENT_ID,
        redirect_uri=credential.REDIRECT_URL,
        scope=SCOPE_USERINFO_PROFILE,
        state=credential.STATE,
    )
    auth_request = AuthRequest(
        params=auth_request_params,
        auth_url=credential.AUTH_URI,
    )

    token_request_params = dto.TokenRequestParams(
        redirect_uri=credential.REDIRECT_URL,
    )
    token_request = TokenRequest(
        params=token_request_params,
        client_id=credential.CLIENT_ID,
        client_secret=credential.CLIENT_SECRET,
        token_uri=credential.TOKEN_URI,
    )


class Services:
    authorization = services.Authorization(
        auth_request=Flow.auth_request,
        token_request=Flow.token_request,
    )


'''
Пример аутентификации и вызова google API.
'''
auth = Services.authorization


@app.route('/')
def login():
    return redirect(auth.get_auth_link())


@app.route('/oauth2/callback/google')
@validate()
def callback_auth_code():
    code = request.args.get('code')
    state = request.args.get('state')

    if state == credential.STATE:
        user_cred = auth.get_user_cred(code)
        session['access_token'] = user_cred.access_token
        return redirect(url_for('get_user_profile'))

    return 'Error authorization'


@app.route('/profile')
def get_user_profile():
    response = requests.get(
        url=API_USERINFO,
        headers=get_header_auth(),
    )
    return response.json()


def get_header_auth():
    token = session['access_token']
    return {'Authorization': 'Bearer {}'.format(token)}
