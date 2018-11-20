FROM python:2.7.15
LABEL maintainer Deming
ENV PYTHONBUFFERED 1
RUN mkdir /genomics-workspace
WORKDIR /genomics-workspace
ADD requirements.txt /genomics-workspace/
RUN pip install -r requirements.txt
CMD ["python","manage.py","runserver"]
