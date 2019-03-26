FROM python:3.7

RUN pip3 install pipenv

WORKDIR /code

COPY Pipfile ./
COPY Pipfile.lock ./

RUN set -ex && pipenv install --deploy --system

COPY . .

EXPOSE 8000
