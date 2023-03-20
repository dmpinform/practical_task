from abc import ABC, abstractmethod

from oauth2.application.dto import AuthData


class AuthRequest(ABC):

    @abstractmethod
    def get_link(self) -> str:
        ...

    def get_request_state(self) -> str:
        ...


class TokenRequest(ABC):

    @abstractmethod
    def get_auth_data(self, code: str) -> AuthData:
        ...
