FROM python:3.13

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /app


COPY ./requirements.txt /app/

RUN --mount=type=cache,target=/root/.cache/pip pip install -r requirements.txt

COPY . /app

CMD ["python", "base_consumer.py"]
