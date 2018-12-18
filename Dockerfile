FROM centos:6.10
LABEL maintainer Deming
ENV PYTHONBUFFERED 1
VOLUME /data
RUN mkdir /genomics-workspace
WORKDIR /genomics-workspace
COPY requirements.txt /genomics-workspace/
RUN yum -y groupinstall "Development tools" && \ 
    yum -y install zlib-devel bzip2-devel openssl-devel ncurses-devel sqlite-devel && \
    yum -y install readline-devel tk-devel gdbm-devel db4-devel libpcap-devel xz-devel python-devel && \    
    yum install wget -y && \
RUN wget http://www.python.org/ftp/python/2.7.15/Python-2.7.15.tar.xz && \ 
    tar -xf Python-2.7.15.tar.xz
RUN cd Python-2.7.15 && \
    ./configure --prefix=/usr/local --enable-unicode=usc4 --enable-shared LDFLAGS="-WL,-rpath /usr/local/lib" && \
    make && \
    make altinstall && \
    wget https://bootstrap.pypa.io/ez_setup.py && \
    /usr/local/bin/python2.7 ez_setup.py && \
    wget https://bootstrap.pypa.io/get-pip.py && \
    /usr/local/bin/python2.7 get-pip.py 
RUN pip install -r requirements.txt && \
    yum install -u gcc-c++ make && \
    curl -sL https://rpm.nodesource.com/setup_10.x \ -E bash - && \
    yum install nodejs
WORKDIR /genomics-workspace    
CMD ["python","manage.py","runserver"]
