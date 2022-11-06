.. TM1 File Tools documentation master file, created by
   sphinx-quickstart on Sun Nov  6 12:04:06 2022.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

TM1 File Tools
==============

**TM1 File Tools** is a Python package that simplifies working with files associated with a
TM1 server. It’s primarily useful for linting or cleaning up a server directory without a dependency on a running TM1 Server.

What it does
------------

-  Scans a TM1 database folder and finds most TM1 related files
   (e.g. ``.cub``, ``.rux`` etc)
-  Provides methods to rename and delete files and properties specific
   to a file type (e.g. the cube a ``.vue`` file refers to)
-  Return lists of “orphaned” files (e.g. a ``.rux`` without a
   corresponding ``.cub``)

What it doesn’t do
------------------

-  Operations on binary files (e.g. it can’t read or edit a ``.cub``
   file)
-  Genuine parsing of text files (e.g. it can’t verify whether a
   ``.rux`` is valid)
-  Interact with the REST API (use
   `TM1py <https://github.com/cubewise-code/tm1py>`__ for that)

.. toctree::
   :maxdepth: 6
   :caption: Contents:

   quickstart
   generated/tm1filetools
   history

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
