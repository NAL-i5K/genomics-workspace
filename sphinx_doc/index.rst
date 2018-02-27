Genomics Workspace
==================

Genomics workspace is a open-source project created by `i5k workspace of NAL
<https://i5k.nal.usda.gov/>`_. In this project, we produced a `Django
<https://www.djangoproject.com/>`_ website with functionality of common sequence searchs including `BLAST
<https://www.ncbi.nlm.nih.gov/books/NBK279690/>`_, `HMMER
<http://hmmer.org/>`_, and `Clustal
<http://www.clustal.org/>`_. Leveraging the `admin page of Django
<https://docs.djangoproject.com/en/1.8/ref/contrib/admin/>`_ and task queue by `RabbitMQ
<https://www.rabbitmq.com/>`_ and `Celery
<http://www.celeryproject.org/>`_, it's much easier to manage the sequence databases and provide services to end-users.



You can try genomics workspace on our live services:

* BLAST: https://i5k.nal.usda.gov/webapp/blast/

* HMMER: https://i5k.nal.usda.gov/webapp/hmmer/

* Clustal: https://i5k.nal.usda.gov/webapp/clustal/


.. toctree::
   :maxdepth: 3
   :numbered:
   :caption: Table of Contents
   :name: mastertoc

   pre_requisites
   setup_guide
   app_conf
   about

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
