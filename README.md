## Практические примеры на Python
***
#### gevente:
- Эксперименты с асинхронностью gevent
#### imports:
- Пример с 3 модулями и импортом через * (с одинкаовым название функций)
#### iterator:
- Реализация итератора
#### network:
- Сеть из трех контейнеров
#### oauth2:
- Реализация code authorization flow с минимальными зависимостями от сторонних пакетов
- Пример вызова API для vk и google
#### package:
- Разработка, упаковка, публикация и установка пакета
#### patterns:
- Разные реализации паттернов
  - decorator
  - factory_method
  - singltone
  - state
  - strategy
### rmq
- Примеры с rabbit mq
- Пример STOMP 
#### Запуск примера:
- запустить RabbitMQ в докере 
- включить плагин docker exec 1bb61ad5fc3f rabbitmq-plugins enable rabbitmq_web_stomp
- запустить тест-страницу```gunicorn rmq.stomp.app:app```
#### Временные очереди STOMP FAQ
- временные очереди: удобно для получения обратного ответа, 
- при отправке сообщения создается две очереди: 1-для задания(в неё попадает сообщение), 2-для ответа, 
- название очереди для ответа прокидывается в заголово reply_to сообщения
- после выполнения задания(обработки сообщения) - ответ возвращается в очередь с именем из reply_to
- очередь для ответа - эксклюзивная (удаляется при отключении клиента, доступна только создателю) - это безопасно и надежно

#### tests:
- Тесты некоторых модулей
#### pre-commit:
- Настроен precommit c хуками: yapf, isort, flake
- Установить: pre-commit~=2.20.0
- Запустить команду: pre-commit install
- Работает для файлов в индексе (после git add .)
