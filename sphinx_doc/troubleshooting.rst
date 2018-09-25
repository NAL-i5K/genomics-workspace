Trouble Shooting
================

Q: I get an error message like: :code:`FATAL: Ident authentication failed`. How can I fix this ?

A: It's because the setting of PostgreSQL database.
Try to modify the config file :code:`pg_hba.conf`.
For example, in PostgreSQL 9.5, the file is at :code:`/var/lib/pgsql/9.5/data/pg_hba.conf`.
Make sure you change part of the content of it into something like:

.. code-block:: none

   local   all             all                               peer
   host    all             all             127.0.0.1/32      ident
   host    all             all             ::1/128           md5
