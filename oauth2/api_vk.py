from oauth2.adapters.api.app import App
from oauth2.adapters.vk.authorization import AuthorizationVk
from oauth2.adapters.vk.settings import Setting
from oauth2.application.services import Authorization
from oauth2.constants import API_STATUS_VK, SCOPE_STATUS_VK
'''
Пример авторизации "auth code flow" и вызова vk API.
'''
setting = Setting()


class Adapter:
    vk_auth = AuthorizationVk(credential=setting, scope=SCOPE_STATUS_VK)


class Service:
    auth_service = Authorization(
        auth=Adapter.vk_auth,
        start_api=API_STATUS_VK,
    )


app = App()
app.add_auth_routes(auth_service=Service.auth_service)
