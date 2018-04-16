Setup Guide (Windows)
=====================

This setup guide is for Windows. It's tested in Windwos 8.1 with django 1.8.12

Note: The following variables may be used in path names; substitute as appropriate::

   <user>      :  the name of the user doing a set up.
   <user-home> :  the user's home directory, e.g., /home/<user>
   <git-home>  :  the directory containing the genomics-workspace, and `.git/` folder for `git` will be there.

Install Git
-----------

* Download: http://git-scm.com/downloads

Project Applications
--------------------

* Download genomics-workspace to a location of your choice, we will use ``C:\`` as an example in the following steps.
* use administrator and run::

   git clone https://github.com/NAL-i5K/genomics-workspace.git
   # Or if the  repository exists:
   cd <git-home>
   git fetch

Microsoft Visual C++
--------------------

* Install Microsoft Visual C++ 9.0 (if you don't have).

* Download from: http://www.microsoft.com/en-us/download/details.aspx?id=44266

Python
------------

* Download from https://www.python.org/downloads/

* The default installation location is ``C:\Python27``, if you did not use the default, modify the following steps accordingly.

* Install pip (if you don't have pip)

   * Download ``get-pip.py``: https://bootstrap.pypa.io/get-pip.py
   * Run ``C:\Python27\python get-pip.py``
   * ``pip.exe`` should now be in ``C:\Python27\Scripts``

* Make sure ``C:\Python27`` and ``C:\Python27\Scripts`` are in your ``PATH`` environment variable.

* Install ``virtualenv``::

   pip install virtualenv

Build a separate virtualenv::

    cd <git-home>
    # Create a virtual environment called py2.7 and activate:
    virtualenv -p C:\Python27\python py2.7
    C:\genomics-workspace\py2.7\Scripts\activate


RabbitMQ
--------

* Before installing the RabbitMQ server, we need to install Erlang, and it can be downloaded from http://www.erlang.org/download.html

* Download RabbitMQ from http://www.rabbitmq.com/download.html

* Start the RabbitMQ service after installation

* Make sure ``C:\Program Files\RabbitMQ Server\rabbitmq_server-3.6.12\sbin`` is in your ``PATH``.


Memcached
---------

* Tutorial: https://commaster.net/content/installing-memcached-windows

Database
--------

Install PostgreSQL, download from * Download: https://www.postgresql.org/download/windows/

* During installation you will needs to set a password for the ``postgres`` superuser, and a connection port (default: 5432) which will be needed in later steps.
* Create a user and a database for django-blast, as an example, we will create a user ``django``, and grant all privileges to ``django`` using the command line tool ``psql``.
* ``psql`` should be at ``Start Menu -> All programs -> PostgreSQL 9.3 -> SQL Shell (psql)``
* Log in, accept the default values by pressing ``enter``, and give it the password for ``postgres`` which was set during installation.
* After logging in, you should see the command prompt ``postgres=#``. Run the following commands, and change ``myPassword`` to something else
* At the prompt ``postgres=#`` enter::

    CREATE USER django WITH PASSWORD 'django1234';
    CREATE DATABASE django
    GRANT ALL PRIVILEGES ON DATABASE django TO django;`
    ALTER USER django CREATEDB;`
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


ChromeDriver
------------
* install ChromeDriver from https://sites.google.com/a/chromium.org/chromedriver/downloads

* add to PATH

Celery
------
Configure the celery::

    # Run celery manually
    celery -A i5k worker --loglevel=info --concurrency=3
    # Run celery beat maually as well
    celery -A i5k beat --loglevel=info


Migrate Schema to to PostgreSQL
-------------------------------

Run migrate::

   cd <git-home>
   `mkdir C:\\var\\log\\django\\`
   `ECHO >> C:\\var\\log\\django\\django.log`
   `ECHO >> C:\\var\\log\\django\\i5k.log`
   `mkdir C:\\[Path to genomics-workspace]\\genomics-workspace\\media\\blast\\db\\`
   # create log files
   sudo mkdir /var/log/django/
   sudo touch /var/log/django/django.log
   sudo touch /var/log/django/i5k.log
   sudo chmod 666 /var/log/django/django.log
   sudo chmod 666 /var/log/i5k/i5k.log
   python manage.py migrate


Install BLAST binary
--------------------

To instll blast binary::

   python setup.py


Start development server
------------------------

To run developement server::

    cd <git-home>
    python manage.py collectstatic
    python manage.py runserver

================================================================================

This section documents the procedure to load organisms into the BLAST database.

PRE-REQUISITES::

    Storage: At least 32 GB of disk space.
    Memory:  At least 10 GB of memory in the system or VM.

To add organism to BLAST you need to download the relevant database files to the
application 'media' directory.

If for example you want to copy the BLAST databases from gmod-dev, make sure
you have at least 32 GB of free disk space.

Also, to run the tool that populates the sequence table you need to have at
least 10 GB of system or VM memory.

In your VM::

    cd <genomics-workspace-dir>/media

    rsync gmod-dev:/usr/local/i5k/media/blast/db/* .

Organisms must be added one at a time using the Django app admin interface.

You need access to a user id with admin privileges.  To do that you must alter
the Postgres database to add such privileges to a normal user.

::

    sudo su postgres
    psql django

First clear any entries that prevent login.

::

    delete from  axes_accessattempt where username='<user_name';

Set your id as superuser

::

    update auth_user set is_staff = 't', is_active = 't' where username = '<user_name>';

Now you should be able to login as admin and navigate to

::

    <your_system>/admin/blast

And then to:

::

    Home » App » Organisms » Add organism

For each organism:

::

    Enter the organism name in the field, 'Display Name'.

    Click in the 'Short Name' and 'Description' fields to have them populated automatically.

    Enter the organism NCBI Taxonomy ID, and click 'SAVE'

    Click on:  BLAST databases 'Add'


Now you must add the databases that correspond to each organism, from those located in:

::

    <genomics-workspace-dir>/media/blast/db/*

Navigate to:

::

   Home » BLAST » BLAST databases

On this screen for each organism:

::

    1. From the top three dropdown lists, select the organism, the type of database type being
       loaded, and 'yes' for 'is_shown.'

    2. Select the database files being loaded in the tabular list of database files.

    3. From the dropdown list next to the 'Go' button, select, 'Populate the sequence table...'
    and click go.

    4. After a while, the three tick marks on each selected row should turn green.



