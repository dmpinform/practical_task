# Настройка сети через docker-compose и проверка
main
one
two

сети service1, service2

main - one, two
one и two не контачат

Результат с http://main-web-app:5500
FROM main-web-app:5500 TO http://one-web-app:5550/ -> Доступен
FROM main-web-app:5500 TO http://two-web-app:5555/ -> Доступен
FROM main-web-app:5500 TO http://one-web-app:5550/ping -> FROM one-web-app:5550 TO http://two-web-app:5555/ -> Не доступен
FROM one-web-app:5550 TO http://main-web-app:5500/ping -> Доступен


# Ручное создание сети
docker network create -d bridge service1
docker network create -d bridge service2

docker run -itd --network=service1 main-web-app
docker run -itd --network=service2 main-web-app
docker run -itd --network=service1 one-web-app 
docker run -itd --network=service2 two-web-app 