FROM alpine:3.4

RUN apk add --update make  python py-pip py-lxml py-requests && \
    pip install --upgrade pip && \
    pip install pytest pytest-cov codecov
