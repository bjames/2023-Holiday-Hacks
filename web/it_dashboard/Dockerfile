FROM python:3.11.7-slim-bullseye

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip
COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt
RUN apt update
RUN apt install -y curl iputils-ping traceroute

RUN mkdir /app
WORKDIR /app
COPY . /app