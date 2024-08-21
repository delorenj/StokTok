FROM python:3.11-alpine3.18

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt /app/

RUN apk add --no-cache ca-certificates && \
    update-ca-certificates && \
    pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements.txt

COPY . /app/