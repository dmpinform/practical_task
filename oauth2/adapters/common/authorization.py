from dataclasses import dataclass
from typing import Dict

import requests

from oauth2.adapters.common.setting import SettingBase
from oauth2.application import dto, interfaces


@dataclass
class Authorization(interfaces.Authorization):
    scope: str
    setting: SettingBase

    def get_request_state(self) -> str:
        return self.setting.STATE

    def get_auth_request(self) -> interfaces.AuthRequest:
        return AuthRequest(
            params=self.get_auth_request_params(),
            auth_uri=self.setting.AUTH_URI,
        )

    def get_token_request(self) -> interfaces.TokenRequest:
        return TokenRequest(
            params=self.get_token_request_params(),
            token_uri=self.setting.TOKEN_URI,
        )

    def get_auth_request_params(self) -> dto.AuthRequestParams:
        return dto.AuthRequestParams(
            client_id=self.setting.CLIENT_ID,
            redirect_uri=self.setting.REDIRECT_URL,
            scope=self.scope,
            state=self.setting.STATE,
        )

    def get_token_request_params(self) -> dto.TokenRequestParams:
        return dto.TokenRequestParams(
            redirect_uri=self.setting.REDIRECT_URL,
            client_id=self.setting.CLIENT_ID,
            client_secret=self.setting.CLIENT_SECRET,
        )


@dataclass
class AuthRequest(interfaces.AuthRequest):
    auth_uri: str
    params: dto.AuthRequestParams

    def get_link(self) -> str:
        auth_link = requests.models.PreparedRequest()
        auth_link.prepare_url(self.auth_uri, self.params.as_dict())
        return auth_link.url


@dataclass
class TokenRequest(interfaces.TokenRequest):
    token_uri: str
    params: dto.TokenRequestParams

    def get_auth_data(self, code: str) -> dto.AuthData:
        auth_data = self._request_auth_data(code)
        return dto.AuthData(access_token=auth_data['access_token'])

    def _request_auth_data(self, code: str):
        return requests.post(
            url=self.token_uri,
            params=self.params.set_code(code).as_dict(),
            headers=self._headers,
        ).json()

    @property
    def _headers(self) -> Dict[str, str]:
        return {'content-type': 'application/x-www-form-urlencoded'}
