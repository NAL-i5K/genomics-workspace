Setup Guide (CentOS)
====================

This setup guide is for CentOS. It's tested in CentOS 6.7 and CentOS 7.2 with django 1.8.12

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
    wget http://www.python.org/ftp/python/2.7.8/Python-2.7.13.tar.xz
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
    virtualenv py2.7
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

Configure the celery::

    # Copy files:
    #
    # When using CentOS 7.* copy
    # celeryd.sysconfig and celerybeat.sysconfig
    # to /etc/default instead.
    #
    sudo cp celeryd /etc/init.d
    sudo cp celerybeat /etc/init.d
    sudo cp celeryd.sysconfig /etc/sysconfig/celeryd
    sudo cp celerybeat.sysconfig /etc/sysconfig/celerybeat

    # Sudo edit '/etc/sysconfig/celeryd' as follows:
    CELERYD_CHDIR="<git-home>"
    CELERYD_MULTI="<git-home>/py2.7/bin/celery multi"

    # Sudo edit '/etc/sysconfig/celerybeat' as follows:
    CELERYBEAT_CHDIR="<git-home>"
    CELERY_BIN="<git-home>/py2.7/bin/celery"

    # Set as daemon:
    sudo chkconfig celeryd on
    sudo chkconfig celerybeat on


Migrate Schema to to PostgreSQL
-------------------------------

Run migrate::

    cd <git-home>
    # create log files
    sudo mkdir /var/log/django/
    sudo touch /var/log/django/django.log
    sudo chmod 666 /var/log/django/django.log
    sudo mkdir /var/log/i5k
    sudo touch /var/log/i5k/i5k.log
    sudo chmod 666 /var/log/i5k/i5k.log
    python manage.py makemigrations
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

Apache (for production server)
------------------------------

Please note:
It is essential that tcp port 80 be open in your system. Sometimes the firewall may deny access to it.
Check if iptables will drop input packets in the output of this command::

    sudo iptables -L

If you see "INPUT" and "DROP" on the same line and no specific ACCEPT rule for tcp port 80
chances are web traffic will be blocked. Ask your sysadmin to open tcp ports 80 and 443 for http and https. Alternatively, check this `iptables guide`_.

.. _iptables guide: https://www.digitalocean.com/community/tutorials/how-to-set-up-a-basic-iptables-firewall-on-centos-6

Install Apache and related modules::

    sudo yum -y install httpd httpd-devel mod_ssl

Give the system a fully qualified domain name (FQDN) if needed::

    # Find out the system IP addres with 'ifconfig'.
    # Assuming it is a VM created by Vagrant, this could be 10.0.2.15.
    # Sudo edit '/etc/hosts' and add an address and domain name entry.
    # For example:
    10.0.2.15  virtualCentOS.local virtualCentOS

    # Sudo edit the file /etc/httpd/conf/httpd.conf,
    # and set the ServerName, for example:
    ServerName virtualCentOS.local:80

    # Set to start httpd at boot:
    sudo chkconfig httpd on

    # Check this setting if you wish, with:
    sudo chkconfig --list httpd

    # Control:
    #    sudo apachectl <command>
    # Where <command> can be:
    #     start         : Start httpd daemon.
    #     stop          : Stop httpd daemon.
    #     restart       : Restart httpd daemon, start it if not running.
    #     status        : Brief status report.
    #     graceful      : Restart without aborting open connections.
    #     graceful-stop : stop without aborting open connections.
    #
    # Start httpd daemon:
    sudo apachectl start

    # Test Apache:
    # If all is well. This command should produce copious
    # HTML output and in the first few lines you should see:
    #   '<title>Apache HTTP Server Test Page powered by CentOS</title>'
    curl localhost

    # You can also view the formatted Apache test page in your
    # browser, e.g., firefox http://<setup-machine-ip-address>


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



