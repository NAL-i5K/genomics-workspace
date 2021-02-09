User Guide
==========

BLAST, HMMER, and Clustal are the main functions of the genomics-workspace. Each of these functions is implemented as a single `app
<https://docs.djangoproject.com/en/1.8/ref/applications/#s-projects-and-applications>`_ under Django.

In this section, we will go through details about how to configure each application.

In short, you need to configure database for BLAST and HMMER, but you don't need to configure anything for Clustal.

.. note:: The page is for users that want to set up genomics-workspace by creating new admin user and confuguring in admin page. **If you want to know how to use services provided by genomics-workspace, see these tutorials:**

   * BLAST: https://i5k.nal.usda.gov/content/blast-tutorial
   * HMMER: https://i5k.nal.usda.gov/webapp/hmmer/manual/
   * CLUSTAL: https://i5k.nal.usda.gov/webapp/clustal/manual/


Getting started
---------------
**To get started, set up the following:**

* setup an admin account

  * Use ``python manage.py createsuperuser``.
  * Follow the instructions shown on your terminal, then browse and login to the admin page of genomics-workspace. Usually, the admin page should be at ``http://127.0.0.1:8000/admin/``.
  * If you already have an admin account, use ``python manage.py runserver`` and then browse and login to genomics-workspace.
  
* All opeations on the command line will be done as the i5k user which is a admin user. You can switch to the i5k user with ``sudo su -l i5k``. You need to be in the apollo group to be able to run this command.

* Create these directories if you don’t have them

  * /usr/local/i5k/media/blast/db/
  * /usr/local/i5k/media/hmmer/db

* Create sequence sequence types in blast/sequence-type. We recommend creating these three:

  * Peptide/Protein
  * Nucleotide/Genome Assembly
  * Nucleotide/Transcript

* Copy all fasta files to be formatted for blast to /usr/local/i5k/media/blast/db/

* Copy protein fasta files to be formatted for hmmer to /usr/local/i5k/media/hmmer/db

BLAST Database Configuration
----------------------------

Manually creating a BLAST database (deprecated)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
* Add Organism (click the **Organism** icon at sidebar and click **Add organism**):

  * Display name should be scientific name.
  * Short name are used by system as a abbreviation.
  * Descriptions and NCBI taxa ID are automatically filled.

.. image:: img/add_organism.png
   :alt: Add organism example

* Add Sequence
* Add BLAST DB

  * Choose ``Organsim``
  * Choose ``Type`` (Sequence type)
  * Type location of fasta file in ``FASTA file path`` (It should be in ``<git-home>/media/blast/db/``)
  * Type ``Title`` name. (showed in HMMER page)
  * Type ``Descriptions``.
  * Check ``is shown``, if not check, this database would show in HMMER page.
  * Save

.. image:: img/add_blastdb.png
   :alt: Add BLAST database example

* Browse to ``http://127.0.0.1:8000/blast/``, you should able to see the page with dataset shown there.

Creating a BLAST database via command line
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
An admin user can add or remove data from the genomics-workspace database via the command line interface. Here, we describe how to use commands to interact with the database.

.. Note:: the order of steps is important. Try to do these steps in order as the i5k user.

1. To add organism

* ``python manage.py addorganism [genus] [species]`` (e.g python manage.py addorganism Apis mellifera)

2. To add a fasta file to the Blast application

*	``python manage.py addblast [genus] [species] -t [type] -f [path of fasta file] -d  [description]`` (e.g python manage.py addblast Apis mellifera -t nucleotide Genome Assembly -f GCF_003254395.2_Amel_HAv3.1_genomic.fna -d Apis mellifera genome assembly, Amel_HAv3.1)
*	[type] here should be one of the sequence types you set up earlier, e.g. "peptide Protein", "nucleotide Genome Assembly" or "nucleotide Transcript"
*	[description] will be the Fasta file description in the web interface. If this argument is omitted, the program will use the Fasta file name. Example descriptions are "[genus] [species] genome assembly, [assembly name]", "[genus] [species] [annotation name], peptides", "[genus] [species] [annotation name], transcripts" or "[genus] [species] [annotation name], CDS"

3.	To make the blast database (via makeblastdb)

*	``python manage.py blast_utility [path of fasta file] -m`` (e.g python manage.py blast_utility media/blast/db/GCF_003254395.2_Amel_HAv3.1_genomic.fna -m)

4.	To populate the genomics-workspace sequences table

* ``python manage.py blast_utility [path of fasta file] -p`` (e.g python manage.py blast_utility media/blast/db/GCF_003254395.2_Amel_HAv3.1_genomic.fna -p)

5. To show the blast database in the web interface (the blast database will not show by default)

* ``python manage.py blast_shown [path of fasta file] -shown ‘true’`` (e.g python manage.py blast_shown media/blast/db/GCF_003254395.2_Amel_HAv3.1_genomic.fna -shown ‘true’)

If you don't see the new organism under the blast webapp, you can login into the postgres database and see if the ``blast_blastdb`` table has the rows with information about your organism.

6. To show the genome in jbrowse

* ``python manage.py addjbrowse [genome assembly fasta file] -shown ‘true’`` (e.g python manage.py addjbrowse GCF_003254395.2_Amel_HAv3.1_genomic.fna https://apollo.nal.usda.gov/apollo/[genus]%20[species]/jbrowse/)


HMMER Database Configuration (deprecated)
----------------------------
Like BLAST, HMMER databases must be configured then they could be searched.

Go to the django admin page and click Hmmer on the left menu bar. You need to create a HMMER db instance (Hmmer dbs) for each fasta file.

Manually creating a HMMER database
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
* Choose ``Organsim``
* Type location of peptide fasta file in ``FASTA file path``
* Type ``Title`` name. (showed in HMMER page)
* Type ``Descriptions``.
* Check ``is shown``, if not check, this database would show in HMMER page.
* Save

.. image:: img/hmmer_add.png
   :alt: Add HMMER database example

Creating a HMMER database via command line
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
An admin user like i5k can add or remove data from the genomics-workspace database via the command line interface. Here, we describe how to use commands to interact with the database.

1.	To add organism (not necessary if the organism is already added)

* ``python manage.py addorganism [genus] [species]`` (e.g python manage.py addorganism Apis mellifera)

2.	To add hmmer database

* ``python manage.py addhmmer [genus] [species] -f [path of fasta file] -d [genus] [species] [annotation name], [sequence type]`` (e.g python manage.py addhmmer Apis mellifera -f  media/blast/db/GCF_003254395.2_Amel_HAv3.1_genomic.fna -d "Apis mellifera Apis_mellifera_Annotation_Release_103, peptides")
* [description] will be the Fasta file description in the web interface. If this argument is omitted, the program will use the Fasta file name. Example description: "[genus][ species] [annotation name], peptides". Note that double quotes are required around the description string otherwise spaces will be ignored.

If you don't see the new organism under the hmmer webapp, you can login into the postgres database and see if the last few rows in the ``hmmer_hmmerdb`` table have information about your organism.

Organism and Database deletion (unavailable)
------------------------------
Organism, BLAST and HMMER databases can be deleted after configuration via the command line interface. Here, we describe the commands for deleting them.

1. To delete organism

* ``python manage.py delete -o [genus] [species]`` (e.g python manage.py delete -o Apis mellifera)

2. To delete BLAST database

* ``python manage.py delete -b [path of fasta file]`` (e.g python manage.py delete -b media/blast/db/GCF_003254395.2_Amel_HAv3.1_genomic.fna)

3. To delete HMMER database

* ``python manage.py delete -h [path of fasta file]`` (e.g python manage.py delete -h media/blast/db/GCF_003254395.2_Amel_HAv3.1_genomic.fna)
