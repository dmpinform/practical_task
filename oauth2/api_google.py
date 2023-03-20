from oauth2.adapters.api.app import App
from oauth2.adapters.google.authorization import AuthorizationGoogle
from oauth2.adapters.google.settings import Setting
from oauth2.application.services import Authorization
from oauth2.constants import API_USERINFO_GOOGLE, SCOPE_USERINFO_PROFILE
'''
Пример авторизации "auth code flow" и вызова google API.
'''

setting = Setting()


class Adapter:
    google_auth = AuthorizationGoogle(
        credential=setting, scope=SCOPE_USERINFO_PROFILE
    )


class Service:
    auth_service = Authorization(
        auth=Adapter.google_auth,
        start_api=API_USERINFO_GOOGLE,
    )


app = App()
app.add_auth_routes(auth_service=Service.auth_service)
