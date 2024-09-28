Clustal Query Histroy
~~~~~~~~~~~~~~~~~~~~~
Clustal query histories are stored in table ``Clustal results``. Users could review them on dashboard.
All query results (files on disk) will be removed if it's expired. (default: after seven days)

Query results locate in directory ``$MEDIA_ROOT/clustal/task/``.

Dashboard
---------

Personal query history.

Data
----
Rest framework. Not finished

Proxy
-----

For providing indirect access to some resources without https. Currently it is used by Web Apollo instances for looking up GO Terms.

Drupal_SSO
----------

Coonection to Drupal summit data function.

::

    DRUPAL_URL = 'https://gmod-dev.nal.usda.gov'

    # cookie can be seen in same domain
    DRUPAL_COOKIE_DOMAIN=".nal.usda.gov"

