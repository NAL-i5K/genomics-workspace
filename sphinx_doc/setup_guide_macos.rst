Setup Guide (MacOS)
===================

This setup guide is tested in MacOS Sierra (10.12) and MacOS High Sierra (10.13), but it should also work on all recent MacOS versions.

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

Homebrew
--------

We recommend to use `Homebrew <https://brew.sh/>`_ as package manager. Installation steps can be found at `https://brew.sh/ <https://brew.sh/>`_.

Python
------------
Install virtualenv::

    pip install virtualenv

Build a separate virtualenv::

    # Make root dir for virtualenv and cd into it:
    cd genomics-workspace

    # Create a virtual environment called py2.7 and activate:
    virtualenv -p python2.7 py2.7
    source py2.7/bin/activate


RabbitMQ
--------

Install and run RabbitMQ Server::

    brew install rabbitmq
    # Make sure /usr/local/sbin is in your $PATH
    rabbitmq-server


Memcached
---------

Install and activate memcached::

   brew install memcached
   memcached


Database
--------

Install PostgreSQL::

    brew install postgres
    psql postgres

    # At the prompt 'postgres=#' enter:
    create database django;
    create user django;
    grant all on database django to django;
    ALTER USER django CREATEDB;

    # Connect to django database:
    \c django

    # Create extension hstore:
    create extension hstore;

    # Exit psql and postgres user:
    \q
    exit


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
    # create log files
    sudo mkdir /var/log/django/
    sudo touch /var/log/django/django.log
    sudo chmod 666 /var/log/django/django.log
    sudo touch /var/log/django/i5k.log
    sudo chmod 666 /var/log/django/i5k.log
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
