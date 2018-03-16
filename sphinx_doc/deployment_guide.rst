How to Deploy
=============

In short, you need to setup following tools and services:

*  `Apache HTTP server
   <https://httpd.apache.org/>`_
*  `mod_wsgi
   <http://modwsgi.readthedocs.io/en/develop/>`_
* RabbitMQ
* Celery daemon

Because genomics workspace is a standard Django website, there is no large difference to deploy genomics workspace.
We recommed to deploy genomics workspace through Apache and mod_wsgi.

You may want take a look the `great documentation of Django project on deploying
<https://docs.djangoproject.com/en/1.8/howto/deployment/>`_ as well.

Apache HTTP server
------------------

RabbitMQ
--------

Celery
------
