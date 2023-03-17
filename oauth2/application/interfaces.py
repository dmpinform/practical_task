from abc import ABC, abstractmethod

from oauth2.application.dto import AuthData


class AuthRequest(ABC):

    @abstractmethod
    def get_link(self) -> str:
        ...


class TokenRequest(ABC):

    @abstractmethod
    def get_auth_data(self, code: str) -> AuthData:
        ...
