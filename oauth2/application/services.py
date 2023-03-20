from dataclasses import dataclass

from oauth2.application import dto, interfaces


@dataclass
class Authorization:
    auth: interfaces.Authorization
    start_api: str

    def get_auth_link(self):
        return self.auth.get_auth_request().get_link()

    def get_user_cred(self, code: str) -> dto.AuthData:
        return self.auth.get_token_request().get_auth_data(code)

    def get_request_state(self) -> str:
        return self.auth.get_request_state()

    def get_start_api(self):
        return self.start_api
