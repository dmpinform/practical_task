## Пример авторизации "auth code flow" и вызова google API и VK API.
- Запускается api указанный по умолчанию, токен сохраняется в сессии Flask 
### VK
- нужно зарегистрировать приложение в vk как сайт
- получить client_id и client_secret
- добавить redirect_url (можно локальный)
- авторизация "code flow" очень ограничена в правах, в отличии от "implict flow"
```
python -m gunicorn oauth2.api_vk:app
```
#### Полекзные ссылки VK
https://dev.vk.com/api/access-token/authcode-flow-user
***
### GOOGLE
- нужно зарегистрировать приложение в google как web application
- получить client_id и client_secret
- добавить redirect_url (можно локальный)
```
python -m gunicorn oauth2.api_google:app
```

#### Полезные ссылки GOOGLE
Сброс разрешений чтобы получить рефреш токен снова
https://myaccount.google.com/u/1/permissions

Создать приложение web application и получить id и secret
https://console.cloud.google.com/apis/credentials

Инструкция 
https://developers.google.com/identity/protocols/oauth2/web-server

Скоупы и апи
https://developers.google.com/identity/protocols/oauth2/scopes

Поиграть с апи
https://developers.google.com/oauthplayground