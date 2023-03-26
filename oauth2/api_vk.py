from oauth2 import constants
from oauth2.adapters.api.app import App
from oauth2.adapters.vk import Authorization, Setting
from oauth2.application import services
'''
Пример авторизации "auth code flow" и вызова vk API.
'''


class Adapter:
    auth = Authorization(
        setting=Setting(),
        scope=constants.SCOPE_STATUS_VK,
    )


class Service:
    auth_service = services.Authorization(
        requests_point=Adapter.auth,
        start_api=constants.API_USERINFO_VK,
    )


app = App()
app.add_auth_routes(auth_service=Service.auth_service)
