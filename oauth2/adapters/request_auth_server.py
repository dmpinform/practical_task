from dataclasses import asdict, dataclass
from typing import Dict

import requests

from oauth2.application import dto, interfaces


@dataclass
class AuthRequest(interfaces.AuthRequest):
    auth_url: str
    params: dto.AuthRequestParams

    def __post_init__(self):
        self.auth_link = requests.models.PreparedRequest()

    def get_link(self) -> str:
        self.auth_link.prepare_url(self.auth_url, asdict(self.params))
        return self.auth_link.url

    def get_request_state(self) -> str:
        return self.params.state


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
