FROM python:2.7-slim

RUN mkdir /genomics-workspace

WORKDIR /genomics-workspace

COPY . /genomics-workspace/

RUN pip install -r requirements.txt



