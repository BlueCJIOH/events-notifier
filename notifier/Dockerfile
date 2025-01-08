FROM python:3.13-alpine

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY ./requirements.txt /app/

RUN --mount=type=cache,target=/root/.cache/pip pip install -r requirements.txt

COPY . /app