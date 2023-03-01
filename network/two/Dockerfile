FROM python:3.9.5-buster

WORKDIR /app

RUN pip install -U pip setuptools

COPY web_app/requirements.txt .
RUN pip install -r requirements.txt

COPY web_app .

CMD ["flask", "run", "--host=0.0.0.0", "--port=5555"]