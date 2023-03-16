from urllib import parse

import requests
from constants import API_USERINFO, SCOPE_USERINFO_PROFILE
from flask import Flask, redirect, request
from requests.auth import HTTPBasicAuth
from settings import Credential

app = Flask(__name__)

credential = Credential()


@app.route('/')
def login():
    return redirect(get_authorization_url())


def get_authorization_url():
    req = requests.models.PreparedRequest()
    params = {
        'client_id': credential.CLIENT_ID,
        'redirect_uri': credential.REDIRECT_URL,
        'scope': SCOPE_USERINFO_PROFILE,
        'state': credential.STATE,
        'response_type': 'code',
    }
    req.prepare_url(credential.AUTH_URI, params)
    return req.url


@app.route('/oauth2/callback/google')
def callback_auth_code():
    params = get_params_url(request.url)
    code = params['code'][0]
    state = params['state'][0]
    if state == credential.STATE:
        token_info = get_token_info(code)
        token = token_info['access_token']
        return get_user_profile(token)
    return 'Error user profile'


def get_user_profile(token):
    headers = {'Authorization': 'Bearer {}'.format(token)}
    response = requests.get(
        url=API_USERINFO,
        headers=headers,
    )
    return response.json()


def get_params_url(url: str):
    query = parse.urlparse(url).query
    return parse.parse_qs(query)


def get_token_info(code: str):
    params = {
        'code': code,
        'grant_type': 'authorization_code',
        'redirect_uri': credential.REDIRECT_URL,
        'prompt': 'consent',
        'access_type': 'offline',
    }
    return requests.post(
        url=credential.TOKEN_URI,
        params=params,
        headers={
            'content-type': 'application/x-www-form-urlencoded'
        },
        auth=HTTPBasicAuth(
            credential.CLIENT_ID,
            credential.CLIENT_SECRET,
        ),
    ).json()
