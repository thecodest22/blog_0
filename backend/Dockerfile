FROM python:3.12-slim
LABEL authors="codest"

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV LANG C.UTF-8

WORKDIR /app

COPY requirements.txt .

RUN mkdir -p logs \
    && pip install --upgrade pip setuptools \
    && pip install --no-cache -r requirements.txt