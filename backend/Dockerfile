FROM python:3.13-alpine

RUN mkdir -p /home/app
RUN mkdir -p /home/app/static

WORKDIR /backend

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY . . 
RUN pip install -r ./requirements.txt
