FROM python:3.9

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PATH "$PATH:/timeofyourlife_v1/"

COPY ./deployment_scripts /deployment_scripts

WORKDIR /timeofyourlife_v1
EXPOSE 8000

COPY Pipfile Pipfile.lock /timeofyourlife_v1/
RUN pip install pipenv && pipenv install --system && \
    mkdir -p /vol/web/static_prod && \
    chmod -R 755 /vol && \
    chmod -R +x /deployment_scripts

COPY . /timeofyourlife_v1/

ENV PATH="/deployment_scripts:$PATH"

CMD ["run.sh"]