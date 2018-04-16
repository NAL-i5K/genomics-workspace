# Sphinx Doc

This folder is for accumulation documents. Most of the files in this folder are used by [Read the Docs](https://readthedocs.org/) (based on [sphinx-doc](http://www.sphinx-doc.org/en/master/sphinx-doc)) to generate our documentation site [http://genomics-workspace.readthedocs.io/en/latest/](http://genomics-workspace.readthedocs.io/en/latest/).

* To generate the documentation offline, run `sphinx-build -b html . _build` in this folder. You will get a documentation sites in `_build` folder. Check the `index.html` inisde there as the starting point.

* Only the stable documentation would be built to form the documentation website. For documentation under development, check the files under `dev_doc` folder in this directory or the `README.md` in different folders.
