FROM python:3.8-alpine as base

FROM base as builder

ARG proxy=""
ENV HTTPS_PROXY $proxy
ENV HTTP_PROXY $proxy

RUN mkdir /install
WORKDIR /install
COPY src/requirements.txt /requirements.txt
RUN apk add --no-cache --update  libxslt-dev libressl-dev gcc musl-dev libffi-dev &&\
    pip install -r /requirements.txt

ENV HTTPS_PROXY ""
ENV HTTP_PROXY ""

COPY src /app
WORKDIR /app
RUN echo -e "0\t*\t*\t*\t*\t export https_proxy=\$GOOGLE_PROXY; python /app/google_calendar_feeder.py" >> /var/spool/cron/crontabs/root && \
    echo -e "*/30\t*\t*\t*\t*\t export https_proxy=\$OUTLOOK_PROXY; python /app/outlook_downloader.py" >> /var/spool/cron/crontabs/root
ENTRYPOINT crond -c /var/spool/cron/crontabs -f -d 0

