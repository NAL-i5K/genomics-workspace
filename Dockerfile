FROM centos:latest

COPY . /usr/local/i5k
WORKDIR /usr/local/i5k

RUN dnf -y install python36-devel python3-pip python3-virtualenv epel-release "@Development Tools" && \
    dnf -y install npm zlib-devel bzip2-devel openssl-devel ncurses-devel sqlite-devel readline-devel pcre pcre-devel && \
    dnf -y install tk-devel gdbm-devel xz-devel libjpeg-turbo libjpeg-turbo-devel zlib libnsl libnsl2 ansible && \
    pip3 install -r requirements.txt