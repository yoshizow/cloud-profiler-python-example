FROM python:3.11-slim-buster

RUN apt-get update && apt-get install -y build-essential

WORKDIR /app

COPY requirements.txt /app

RUN pip install --upgrade pip && pip install -r requirements.txt

COPY main.py /app

ARG GOOGLE_CLOUD_PROJECT
ENV GOOGLE_CLOUD_PROJECT=$GOOGLE_CLOUD_PROJECT

CMD ["bash"]
