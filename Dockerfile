FROM python:3.8

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ENV LANG fa_IR.UTF-8
ENV LC_ALL=fa_IR

WORKDIR /my_site

COPY Pipfile Pipfile.lock /my_site/
RUN pip install pipenv && pipenv install --system




COPY . /my_site/