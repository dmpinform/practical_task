from dataclasses import dataclass
from typing import Dict

import requests

from oauth2.application import dto


@dataclass
class AuthRequest:
    auth_url: str
    params: dto.AuthRequestParams

    def __post_init__(self):
        self.auth_link = requests.models.PreparedRequest()

    def get_link(self) -> str:
        self.auth_link.prepare_url(self.auth_url, self.params.as_dict())
        return self.auth_link.url


@dataclass
class TokenRequest:
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
