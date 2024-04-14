FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /avitotech

COPY ./requirements.txt /avitotech/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /avitotech/requirements.txt

# 
COPY . /avitotech