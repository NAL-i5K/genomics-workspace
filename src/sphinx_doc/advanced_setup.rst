Advanced Setup
==============

JBrowse/Apollo Linkout Integration
----------------------------------

In Genomics workspace, we have a linkout integration between BLAST and JBrowse/Apollo.
You can directly go to corresponding sequence location through clicking entries in BLAST result table.
To start using it, make change of :code:`ENABLE_JBROWSE_INTEGRATION` in :code:`i5k/settings.py`;

.. code-block:: python

   ENABLE_JBROWSE_INTEGRATION = True
