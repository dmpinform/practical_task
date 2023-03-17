from dataclasses import dataclass
from typing import Optional


@dataclass
class AuthRequestParams:
    client_id: str
    redirect_uri: str
    scope: str
    state: str
    response_type: str = 'code'


@dataclass
class TokenRequestParams:
    redirect_uri: str
    grant_type: str = 'authorization_code'
    prompt: str = 'consent'
    access_type: str = 'offline'
    code: Optional[str] = None


@dataclass
class AuthData:
    access_token: str
