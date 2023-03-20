from oauth2.adapters.api.app import App
from oauth2.adapters.request_auth_server import AuthRequest, TokenRequest
from oauth2.adapters.google.settings import Credential
from oauth2.application import dto, services
from oauth2.constants import SCOPE_USERINFO_PROFILE

credential = Credential()


class Flow:
    auth_request_params = dto.AuthRequestParams(
        client_id=credential.CLIENT_ID,
        redirect_uri=credential.REDIRECT_URL,
        scope=SCOPE_USERINFO_PROFILE,
        state=credential.STATE,
    )
    auth_request = AuthRequest(
        params=auth_request_params,
        auth_url=credential.AUTH_URI,
    )

    token_request_params = dto.TokenRequestParams(
        redirect_uri=credential.REDIRECT_URL,
        client_id=credential.CLIENT_ID,
        client_secret=credential.CLIENT_SECRET,
    )
    token_request = TokenRequest(
        params=token_request_params,
        token_uri=credential.TOKEN_URI,
    )


class Services:
    authorization = services.Authorization(
        auth_request=Flow.auth_request,
        token_request=Flow.token_request,
    )


'''
Пример аутентификации и вызова google API.
'''
app = App()
app.add_auth_routes(auth_service=Services.authorization)
