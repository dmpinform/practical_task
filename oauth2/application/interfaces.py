from abc import ABC, abstractmethod

from oauth2.application import dto
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


class Authorization(ABC):

    @abstractmethod
    def get_auth_request(self) -> AuthRequest:
        ...

    @abstractmethod
    def get_token_request(self) -> TokenRequest:
        ...

    @abstractmethod
    def get_request_state(self) -> str:
        ...

    @abstractmethod
    def get_auth_request_params(self) -> dto.AuthRequestParams:
        ...

    @abstractmethod
    def get_token_request_params(self) -> dto.TokenRequestParams:
        ...
