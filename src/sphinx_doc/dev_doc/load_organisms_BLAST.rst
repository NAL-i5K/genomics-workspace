Windows
=======

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



MacOS
=====

This section documents the procedure to load organisms into the BLAST database.

PRE-REQUISITES.

::

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

On this screen for each organism::

    1. From the top three dropdown lists, select the organism, the type of database type being
       loaded, and 'yes' for 'is_shown.'

    2. Select the database files being loaded in the tabular list of database files.

    3. From the dropdown list next to the 'Go' button, select, 'Populate the sequence table...'
    and click go.

    4. After a while, the three tick marks on each selected row should turn green.



CentOS
======

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
