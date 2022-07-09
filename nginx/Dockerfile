FROM nginxinc/nginx-unprivileged:latest

COPY ./default.conf.tpl /etc/nginx/default.conf.tpl
COPY ./uwsgi_params /etc/nginx/uwsgi_params
COPY ./run.sh /run.sh

ENV LISTEN_PORT=8000
ENV APP_HOST=web
ENV APP_PORT=9000

USER root

RUN mkdir -p /vol/static_prod && \
    chmod 755 /vol/static_prod && \
    touch /etc/nginx/conf.d/default.conf && \
    chown nginx:nginx /etc/nginx/conf.d/default.conf && \
    chmod +x /run.sh

VOLUME /vol/static_prod

CMD ["/run.sh"]