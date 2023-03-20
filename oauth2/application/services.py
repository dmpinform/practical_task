from dataclasses import dataclass

from oauth2.application import dto, interfaces


@dataclass
class Authorization:
    auth_request: interfaces.AuthRequest
    token_request: interfaces.TokenRequest

    def get_auth_link(self):
        return self.auth_request.get_link()

    def get_user_cred(self, code: str) -> dto.AuthData:
        return self.token_request.get_auth_data(code)

    def get_request_state(self) -> str:
        return self.auth_request.get_request_state()
