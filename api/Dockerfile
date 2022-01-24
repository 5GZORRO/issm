FROM python:3.6.5-alpine

RUN apk add --no-cache bash \
 && apk add --no-cache --virtual .build-deps \
        bzip2-dev \
        g++ \
        libc-dev

RUN pip install --upgrade pip setuptools

RUN pip install --no-cache-dir gevent==1.2.1 flask>=1.0.0 requests==2.13.0 kubernetes==10.0.1 kafka-python==2.0.2 iso8601==1.0.2 \
  && apk del .build-deps

RUN mkdir -p /issmApi
ADD server.py /issmApi/

CMD ["/bin/bash", "-c", "cd issmApi && python -u server.py"]
