FROM python:2.7-slim

RUN mkdir /genomics-workspace

WORKDIR /genomics-workspace

COPY . /genomics-workspace/

RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["usr/local/bin/python","/genomics-workspace/manage.py","makemigrations"]

CMD ["/usr/local/bin/python","/genomics-workspace/manage.py","migrate"]

CMD ["/usr/local/bin/python","/genomics-workspace/manage.py","runserver","0.0.0.0:8000"]
