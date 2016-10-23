FROM alpine:3.4

RUN apk add --update python py-pip make && \
    pip install --upgrade pip && \
    apk --update add --virtual build-deps python-dev build-base libxml2-dev libxslt-dev && \
    pip install requests lxml pytest pytest-cov codecov && \
    apk del build-deps
