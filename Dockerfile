FROM python:3.9

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PATH "$PATH:/timeofyourlife_v1/"

WORKDIR /timeofyourlife_v1

COPY Pipfile Pipfile.lock /timeofyourlife_v1/
RUN pip install pipenv && pipenv install --system

COPY . /timeofyourlife_v1/