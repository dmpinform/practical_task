import requests
from flask import Flask

app = Flask(__name__)

HOSTS = [
    'http://one-web-app:5550/',
    'http://two-web-app:5555/',
    'http://one-web-app:5550/ping',
]


@app.route('/')
def services_network():
    return batch_ping()


@app.get('/ping')
def services_network_ping():
    return 'Доступен'


def batch_ping():
    result: str = ''
    for url in HOSTS:
        result += f'FROM main-web-app:5500 TO {url} -> {ping(url)}<br>'
    return result


def ping(url):
    return requests.get(url=url).text
