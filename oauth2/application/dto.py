from dataclasses import asdict, dataclass, field
from typing import Optional


@dataclass
class AuthRequestParams:
    client_id: str
    redirect_uri: str
    state: str
    response_type: str = 'code'
    scope: Optional[str] = None

    def as_dict(self):
        return asdict(self)


@dataclass
class TokenRequestParams:
    redirect_uri: str
    client_id: str
    client_secret: str
    grant_type: str = 'authorization_code'
    code: str = field(init=False)

    def set_code(self, code: str) -> 'TokenRequestParams':
        self.code = code
        return self

    def as_dict(self):
        return asdict(self)


@dataclass
class AuthData:
    access_token: str
    id_token: Optional[str]
