## Создание сети через docker-compose
*Для большей наглядности адресации написаны микро приложения на Flask*
- Создать три Flask приложения c перекрестными эндпоинтами 
- Создать три контейнера: web, one, two
- Создать две сети service1, service2
- Включить контейнеры в разные сети
- Проверить доступ между контейнерами и изоляцию сетей

## Ручное создание сети
- docker network create -d bridge service1
- docker network create -d bridge service2
- docker run -itd --network=service1 main-web-app
- docker run -itd --network=service2 main-web-app
- docker run -itd --network=service1 one-web-app 
- docker run -itd --network=service2 two-web-app 

## Проверка 
- Поднять контейнеры `docker-compose up` и пройти по ссылкам
- *http://127.0.0.1:5500*
  - FROM main-web-app:5500 TO http://one-web-app:5550/ping -> Доступен
  - FROM main-web-app:5500 TO http://two-web-app:5555/ping -> Доступен
- *http://127.0.0.1:5550*
  - FROM one-web-app:5550 TO http://two-web-app:5555/ping -> Не доступен
  - FROM one-web-app:5550 TO http://main-web-app:5500/ping -> Доступен
- *http://127.0.0.1:5555*
  - FROM two-web-app:5555 TO http://one-web-app:5550/ping -> Не доступен
  - FROM two-web-app:5555 TO http://main-web-app:5500/ping -> Доступен
