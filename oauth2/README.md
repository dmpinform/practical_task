## Пример авторизации "auth code flow" и вызова google API и VK API.
- Запускается api указанный по умолчанию, токен доступа сохраняется в сессии Flask
- Для Google также в сессию сохраняется id_token(JWT, содержащий информацию о пользователе)
### VK
- нужно зарегистрировать приложение в vk как сайт
- получить client_id и client_secret
- добавить redirect_url (можно локальный)
- внедрить переменных окружения .env.example
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
- добавить тестовых пользователей
- внедрить переменных окружения .env.example
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
