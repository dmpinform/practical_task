import requests
from flask import Flask

app = Flask(__name__)


@app.route('/')
def services_network():
    return 'Доступен'


HOSTS = [
    'http://two-web-app:5555/',
    'http://main-web-app:5500/ping',
]


@app.get('/ping')
def services_network_ping():
    return batch_ping()


def batch_ping():
    result: str = ''
    for url in HOSTS:
        result += f'FROM one-web-app:5550 TO {url} -> {ping(url)}<br>'
    return result


def ping(url):
    try:
        return requests.get(url=url).text
    except:
        return 'Не доступен'
