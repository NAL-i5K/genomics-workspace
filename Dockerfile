FROM centos:6.10
LABEL maintainer Deming
ENV PYTHONBUFFERED 1
VOLUME /data
RUN mkdir /genomics-workspace
WORKDIR /genomics-workspace
COPY requirements.txt /genomics-workspace/
RUN yum groupinstall "Development tools" -y && \ 
    yum install wget -y
RUN wget http://www.python.org/ftp/python/2.7.15/Python-2.7.15.tar.xz && \ 
    tar -xf Python-2.7.15.tar.xz
RUN yum install automake && \ 
    yum install autoconf && \
    cd Python-2.7.15 && \
    ./configure --prefix=/usr/local --enable-unicode=usc4 --enable-shared LDFLAGS="-WL,-rpath /usr/local/lib" && \
    make && \
    make altinstall
RUN pip install -r requirements.txt
CMD ["python","manage.py","runserver"]
