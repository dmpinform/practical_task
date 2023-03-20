from dataclasses import dataclass

from oauth2.adapters.common.request_auth_server import AuthRequest, TokenRequest
from oauth2.adapters.common.setting import SettingBase
from oauth2.application import dto, interfaces


@dataclass
class Authorization(interfaces.Authorization):
    scope: str
    credential: SettingBase

    def get_request_state(self) -> str:
        return self.credential.STATE

    def get_auth_request(self) -> interfaces.AuthRequest:
        return AuthRequest(
            params=self._get_auth_request_params(self.scope),
            auth_url=self.credential.AUTH_URI,
        )

    def get_token_request(self) -> interfaces.TokenRequest:
        return TokenRequest(
            params=self._get_token_request_params(),
            token_uri=self.credential.TOKEN_URI,
        )

    def _get_auth_request_params(self, scope):
        return dto.AuthRequestParams(
            client_id=self.credential.CLIENT_ID,
            redirect_uri=self.credential.REDIRECT_URL,
            scope=scope,
            state=self.credential.STATE,
        )

    def _get_token_request_params(self):
        return dto.TokenRequestParams(
            redirect_uri=self.credential.REDIRECT_URL,
            client_id=self.credential.CLIENT_ID,
            client_secret=self.credential.CLIENT_SECRET,
        )
