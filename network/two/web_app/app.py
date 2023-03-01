from flask import Flask

app = Flask(__name__)


@app.route('/')
def services_network():
    return 'Доступен'
