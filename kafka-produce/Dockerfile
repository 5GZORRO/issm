FROM python:3.6.1-alpine

# Upgrade and install basic Python dependencies.
RUN apk add --no-cache bash \
 && apk add --no-cache --virtual .build-deps \
        bzip2-dev \
        gcc \
        libc-dev \
  && pip install --upgrade pip setuptools \
  && pip install --no-cache-dir kafka-python==1.4.2 requests==2.13.0 \
  && apk del .build-deps
