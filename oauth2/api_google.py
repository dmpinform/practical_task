from oauth2 import constants
from oauth2.adapters.api.app import App
from oauth2.adapters.google import Authorization, Setting
from oauth2.application import services
'''
Пример авторизации "auth code flow" и вызова google API.
'''


class Adapter:
    auth = Authorization(
        setting=Setting(),
        scope=constants.SCOPE_USERINFO_PROFILE,
    )


class Service:
    auth_service = services.Authorization(
        requests_point=Adapter.auth,
        start_api=constants.API_USERINFO_GOOGLE,
    )


app = App()
app.add_auth_routes(auth_service=Service.auth_service)
