# syntax=docker/dockerfile:1
FROM python:3-slim
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

VOLUME ["/code"]
WORKDIR /code

COPY requirements.txt .
RUN pip install -r requirements.txt
#COPY . /code/