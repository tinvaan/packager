FROM python:3.7-slim

RUN apt-get update && apt-get install -y build-essential python3-dev

RUN mkdir -p /packager
WORKDIR /packager
COPY . /packager

ENV PYTHONPATH $(pwd):$PYTHONPATH
RUN pip install -r requirements.txt
