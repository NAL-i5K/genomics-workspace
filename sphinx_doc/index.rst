Genomics Workspace
==================

Genomics workspace is a open-source project created by `i5k workspace of NAL
<https://i5k.nal.usda.gov/>`_.

In this project, we produced a `Django
<https://www.djangoproject.com/>`_ website with functionality of common sequence searchs including `BLAST
<https://www.ncbi.nlm.nih.gov/books/NBK279690/>`_, `HMMER
<http://hmmer.org/>`_, and `Clustal
<http://www.clustal.org/>`_.

Leveraging the `admin page of Django
<https://docs.djangoproject.com/en/1.8/ref/contrib/admin/>`_ and task queue by `RabbitMQ
<https://www.rabbitmq.com/>`_ and `Celery
<http://www.celeryproject.org/>`_, it's much easier to manage the sequence databases and provide services to end-users.

All source codes of genomics workspace are in `our github repo
<https://github.com/NAL-i5K/genomics-workspace/>`_.

.. note::
   You can try genomics workspace on our live services:

   * BLAST: https://i5k.nal.usda.gov/webapp/blast/
   * HMMER: https://i5k.nal.usda.gov/webapp/hmmer/
   * Clustal: https://i5k.nal.usda.gov/webapp/clustal/

   In fact, the live services listed above are implemented by a customized version of genomics workspace.
   You can check the source code of it in another github repo: `NAL-genomics-workspace
   <https://github.com/NAL-i5K/NAL-genomics-workspace>`_.


.. toctree::
   :maxdepth: 2
   :numbered:
   :caption: Table of Contents
   :name: mastertoc

   pre_requisites
   setup_guide
   user_guide
   deployment_guide
   docker_setup
   troubleshooting
   about

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
