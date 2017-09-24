Setup Guide (MacOS)
===================

This setup guide is tested in MacOS Sierra (10.12.6) with django 1.8.12.

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
    virtualenv py2.7 
    source py2.7/bin/activate
    
    
RabbitMQ
--------

Install RabbitMQ Server::

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

    brew postgres
    psql postgres
    
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


Python Modules and Packages
---------------------------

Install additional Python packages::

    cd <git-home>
    pip install -r requirements.txt

Celery
------

Configure celery::

    # Run celery manually:
    celery -A i5k worker --loglevel=info

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
    python manage.py makemigrations
    python manage.py migrate

Start development server
------------------------

To run developement server::

    cd <git-home>
    python manage.py runserver


================================================================================

This section documents the procedure to load organisms into the BLAST database. 

PRE-REQUISITES.  

    Storage: At least 32 GB of disk space. 
    Memory:  At least 10 GB of memory in the system or VM. 

To add organism to BLAST you need to download the relevant database files to the 
application 'media' directory.  

If for example you want to copy the BLAST databases from gmod-dev, make sure 
you have at least 32 GB of free disk space.  

Also, to run the tool that populates the sequence table you need to have at 
least 10 GB of system or VM memory.  

    In your VM: 

    cd <genomics-workspace-dir>/media

    rsync gmod-dev:/usr/local/i5k/media/blast/db/* .

Organisms must be added one at a time using the Django app admin interface. 

You need access to a user id with admin privileges.  To do that you must alter 
the Postgres database to add such privileges to a normal user. 

    sudo su postgres
    psql django 

First clear any entries that prevent login. 

    delete from  axes_accessattempt where username='<user_name';

Set your id as superuser

    update auth_user set is_staff = 't', is_active = 't' where username = '<user_name>';

Now you should be able to login as admin and navigate to 

    <your_system>/admin/blast

And then to: 

    Home » App » Organisms » Add organism 

For each organism: 

    Enter the organism name in the field, 'Display Name'.

    Click in the 'Short Name' and 'Description' fields to have them populated automatically. 

    Enter the organism NCBI Taxonomy ID, and click 'SAVE'

    Click on:  BLAST databases 'Add'  


Now you must add the databases that correspond to each organism, from those located in: 

    <genomics-workspace-dir>/media/blast/db/*

Navigate to: Home » BLAST » BLAST databases 

On this screen for each organism: 

    1. From the top three dropdown lists, select the organism, the type of database type being 
       loaded, and 'yes' for 'is_shown.' 

    2. Select the database files being loaded in the tabular list of database files.  

    3. From the dropdown list next to the 'Go' button, select, 'Populate the sequence table...' and click go.

    4. After a while, the three tick marks on each selected row should turn green.  



