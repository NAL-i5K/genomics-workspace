FROM python:2.7-slim

ENV PYTHONUNBUFFERED 1

RUN mkdir /genomics-workspace

WORKDIR /genomics-workspace

RUN apt-get update && apt-get upgrade -y && apt-get install -y libsqlite3-dev

RUN pip install -U pip setuptools

COPY . /genomics-workspace/

RUN pip install -r requirements.txt

EXPOSE 8000

RUN pwd

CMD ["python","manage.py","migrate"]

CMD ["python","manage.py","collectstatic","--noinput"]

CMD ["python","manage.py","runserver","0.0.0.0:8000"]
