# Genomic-Workspace

[![Build Status](https://travis-ci.org/NAL-i5K/genomics-workspace.svg?branch=master)](https://travis-ci.org/NAL-i5K/genomics-workspace/?branch=master)
[![codecov](https://codecov.io/gh/NAL-i5K/genomics-workspace/branch/master/graph/badge.svg)](https://codecov.io/gh/NAL-i5K/genomics-workspace)
[![codebeat badge](https://codebeat.co/badges/2a92682c-1434-4ab2-ba27-f2d750819356)](https://codebeat.co/projects/github-com-nal-i5k-genomics-workspace-master)
[![Documentation Status](http://readthedocs.org/projects/genomics-workspace/badge/?version=latest)](http://genomics-workspace.readthedocs.io/en/latest/)

Genomics-Workspace is a bioinformatic website project created by [i5k Workspace](https://i5k.nal.usda.gov/). It provides common sequence search services including [BLAST](http://blast.ncbi.nlm.nih.gov/Blast.cgi?PAGE_TYPE=BlastDocs&DOC_TYPE=Download), [HMMER](http://hmmer.org/), and [Clustal](http://www.clustal.org/). To see it in action, please visit following live sites:

* BLAST: [https://i5k.nal.usda.gov/webapp/blast/](https://i5k.nal.usda.gov/webapp/blast/)
* HMMER: [https://i5k.nal.usda.gov/webapp/hmmer/](https://i5k.nal.usda.gov/webapp/hmmer/)
* Clustal: [https://i5k.nal.usda.gov/webapp/clustal/](https://i5k.nal.usda.gov/webapp/clustal/)

## Features

### Backend

* Implemented in [Python](https://www.python.org/) with [Django](https://www.djangoproject.com/).
* Supports searches for [BLAST](http://blast.ncbi.nlm.nih.gov/Blast.cgi?PAGE_TYPE=BlastDocs&DOC_TYPE=Download), [HMMER](http://hmmer.org/), and [Clustal](http://www.clustal.org/).
* Task queue with [Celery](https://github.com/celery/celery) and [RabbitMQ](http://www.rabbitmq.com/).
* Use [PostgreSQL](https://www.postgresql.org/) as database backend.
* BLAST:
  * Generates several BLAST output formats for download: Text, TSV, XML, ASN.1.
  * Converts BLAST output to GFF3 by grouping contiguous HSPs with identical query sequence, subject sequence, strand direction and an overlap length less than 6 between neighbouring HSPs under the same match.
* Retrieve previous results with a unique URL for every task.
* Supports both Linux and MacOS.

### Frontend

* Special BLAST visualization powered by [D3.js](https://d3js.org/) and [JQuery](http://jquery.com/).
  * The results page is an interactive data viewer, query and subject coverage graphs on the top are drawn dynamically on the HTML5 canvas for every high scoring pair (HSP), tabular output from BLAST+ is displayed in a sortable and searchable table on the bottom right, pairwise text output is displayed on the bottom left panel.
  * Fullscreen design dynamically scales to any screen size
  * Dynamically draws a unique query coverage graph and a subject coverage graph for every high scoring pair(HSP) on HTML5 canvas.
  * Interactive graph updates the page as the user mouse over each aligned segment.
  * Graph zoom level and line height are first calculated according to the data and screen size, but can be easily adjusted to user's preference using the sliders on the left and right sides of each graph.
  * Interactive results table updates the page as the user:
    * Mouse over each row.
    * Changes the sorting column.
    * Filters the table using the search box.

## Screenshots

BLAST Results
![BLAST Results](sphinx_doc/img/blast-results-dynamic.gif)

## Documentation

Docs can be found at [genomics-workspace.readthedocs.io](https://genomics-workspace.readthedocs.io/en/latest/).

## How to contribute

You're highly encouraged to participate in the development of genomics-workspace. Check the [CONTRIBUTING.md](CONTRIBUTING.md) first and start contributing !
