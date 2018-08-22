How to Deploy
=============

In short, you need to setup following tools and services:

* `Apache HTTP server
  <https://httpd.apache.org/>`_
* `mod_wsgi
  <http://modwsgi.readthedocs.io/en/develop/>`_
* `RabbitMQ
  <https://www.rabbitmq.com/>`_
* `Celery and celerybeat
  <https://github.com/celery/celery>`_ runs in daemon mode.

Because genomics workspace is a standard Django website, there is no large difference to deploy genomics workspace.
We recommed to deploy genomics workspace through Apache and mod_wsgi.

You may want take a look the `great documentation of Django project on deploying
<https://docs.djangoproject.com/en/1.8/howto/deployment/>`_ as well.

Apache HTTP server and mod_wsgi
-------------------------------

See the `document of Django
<https://docs.djangoproject.com/en/1.8/howto/deployment/wsgi/modwsgi/>`_. You can also see the example settings file of Apache and mod_wsgi `in our github repo
<https://github.com/NAL-i5K/genomics-workspace/blob/4ec1f58020d00a38ccb7ffbc6b071bf5abca4390/example/settings/i5k.conf>`_.


RabbitMQ
--------

Use the `rabbitmq-server command
<https://www.rabbitmq.com/rabbitmq-server.8.html>`_.

Celery and celerybeat
---------------------

Here are example setup steps for linux,

1. Copy files::

    # when using CentOS 7.*
    # copy celeryd.sysconfig and celerybeat.sysconfig to /etc/default instead.
    sudo cp celeryd /etc/init.d
    sudo cp celerybeat /etc/init.d
    sudo cp celeryd.sysconfig /etc/sysconfig/celeryd
    sudo cp celerybeat.sysconfig /etc/sysconfig/celerybeat

2. edit '/etc/sysconfig/celeryd'::

    CELERYD_CHDIR="<git-home>"
    CELERYD_MULTI="<git-home>/py2.7/bin/celery multi"

3. edit '/etc/sysconfig/celerybeat' as follows::

    CELERYBEAT_CHDIR="<git-home>"
    CELERY_BIN="<git-home>/py2.7/bin/celery"

4. set as daemon::

    sudo chkconfig celeryd on
    sudo chkconfig celerybeat on

For more details or setup on Mac, check the `document of Celery
<http://docs.celeryproject.org/en/3.1/tutorials/daemonizing.html>`_. Example files mentioned above are also (celery*) `in our github repo
<https://github.com/NAL-i5K/genomics-workspace/tree/4ec1f58020d00a38ccb7ffbc6b071bf5abca4390/example/settings>`_.
