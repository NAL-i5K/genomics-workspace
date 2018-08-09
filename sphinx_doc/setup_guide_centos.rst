Setup Guide (CentOS)
====================

This setup guide is for CentOS. It's tested in CentOS 6.7 and CentOS 7.2, but it should also work on all modern linux distributions.

Note: The following variables may be used in path names; substitute as appropriate::

   <user>      :  the name of the user doing a set up.
   <user-home> :  the user's home directory, e.g., /home/<user>
   <git-home>  :  the directory containing the genomics-workspace, and `.git/` folder for `git` will be there.

Project Applications
--------------------

Clone or refresh the genomics-workspace::

    git clone https://github.com/NAL-i5K/genomics-workspace

    # Or if the  repository exists:
    cd <git-home>
    git fetch

Yum
---

Generate metadata cache::

    yum makecache

Python
------------

Install necessary packages::

    sudo yum -y groupinstall "Development tools"
    sudo yum -y install zlib-devel bzip2-devel openssl-devel ncurses-devel sqlite-devel
    sudo yum -y install readline-devel tk-devel gdbm-devel db4-devel libpcap-devel xz-devel python-devel

Install python 2.7.13 from source::

    cd <user-home>
    wget http://www.python.org/ftp/python/2.7.13/Python-2.7.13.tar.xz
    tar -xf Python-2.7.13.tar.xz

    # Configure as a shared library:
    cd Python-2.7.13
    ./configure --prefix=/usr/local --enable-unicode=ucs4 --enable-shared LDFLAGS="-Wl,-rpath /usr/local/lib"

    # Compile and install:
    make
    sudo make altinstall

    # Update PATH:
    export PATH="/usr/local/bin:$PATH"

    # Checking Python version (output should be: Python 2.7.13):
    python2.7 -V

    # Cleanup if desired:
    cd ..
    rm -rf Python-2.7.13.tar.xz Python-2.7.13

Install pip and virtualenv::

    wget https://bootstrap.pypa.io/ez_setup.py
    sudo /usr/local/bin/python2.7 ez_setup.py

    wget https://bootstrap.pypa.io/get-pip.py
    sudo /usr/local/bin/python2.7 get-pip.py

    sudo /usr/local/bin/pip2.7 install virtualenv

Build a separate virtualenv::

    cd <git-home>

    # Create a virtual environment called py2.7 and activate:
    virtualenv -p python2.7 py2.7
    source py2.7/bin/activate


RabbitMQ
--------

Install RabbitMQ Server::

    cd <user-home>

    # Install RHEL/CentOS 6.8 64-Bit Extra Packages for Enterprise Linux (Epel).
    # The 6.8 Epel caters for CentOS 6.*:
    wget https://dl.fedoraproject.org/pub/epel/6/x86_64/epel-release-6-8.noarch.rpm
    sudo rpm -ivh epel-release-6-8.noarch.rpm

    # For RHEL/CentOS 7.* :
    # wegt http://dl.fedoraproject.org/pub/epel/7/x86_64/e/epel-release-7-10.noarch.rpm
    # and change other commands accordingly

    # Install Erlang:
    sudo yum -y install erlang

    # Install RabbitMQ server:
    sudo yum -y install rabbitmq-server

    # To start the daemon by default when system boots run:
    sudo chkconfig rabbitmq-server on

    # Start the server:
    sudo /sbin/service rabbitmq-server start

    # Clean up:
    rm epel-release-6-8.noarch.rpm


Memcached
---------

Install and activate memcached::

   sudo yum -y install memcached

   # Set to start at boot time:
   sudo chkconfig memcached on

Database
--------

Install PostgreSQL::

    # Add line to yum repository:
    echo 'exclude=postgresql*' | sudo tee -a /etc/yum.repos.d/CentOS-Base.repo

    # Install the PostgreSQL Global Development Group (PGDG) RPM file:
    sudo yum -y install http://yum.postgresql.org/9.5/redhat/rhel-6-x86_64/pgdg-centos95-9.5-2.noarch.rpm

    # Install PostgreSQL 9.5:
    sudo yum -y install postgresql95-server postgresql95-contrib postgresql95-devel

    # Initialize (uses default data directory: /var/lib/pgsql):
    sudo service postgresql-9.5 initdb

    # Startup at boot:
    sudo chkconfig postgresql-9.5 on

    # Control:
    # sudo service postgresql-9.5 <command>
    #
    # where <command> can be:
    #
    #     start   : start the database.
    #     stop    : stop the database.
    #     restart : stop/start the database; used to read changes to core configuration files.
    #     reload  : reload pg_hba.conf file while keeping database running.

    # Start:
    sudo service postgresql-9.5 start

    #
    #  (To remove everything: sudo yum erase postgresql95*)
    #

    # Create django database and user:
    sudo su - postgres
    psql

    # At the prompt 'postgres=#' enter:
    create database django;
    create user django;
    grant all on database django to django;

    # Connect to django database:
    \c django

    # Create extension hstore:
    create extension hstore;

    # Exit psql and postgres user:
    \q
    exit

    # Config in pg_hba.conf:
    cd <git-home>
    export PATH=/usr/pgsql-9.5/bin:$PATH

    # Restart:
    sudo service postgresql-9.5 restart


Python Modules and Packages
---------------------------

Install additional Python packages::

    cd <git-home>
    pip install -r requirements.txt

Chrome Driver
-------------
* Install ChromeDriver from https://sites.google.com/a/chromium.org/chromedriver/downloads

* Add to PATH

Celery
------

Configure celery::

    # Run celery manually
    celery -A i5k worker --loglevel=info --concurrency=3
    # Run celery beat maually as well
    celery -A i5k beat --loglevel=info


Migrate Schema to to PostgreSQL
-------------------------------

Run migrate::

    cd <git-home>
    python manage.py migrate


Install BLAST binary
--------------------

To instll blast binary::

   python setup.py


Start development server
------------------------

To run developement server::

    cd <git-home>
    python manage.py runserver
