TM1 File Tools
==============

**TM1 File Tools** Python package that simplifies working with files associated with a
TM1 server. It’s primarily useful for linting or cleaning up a server
directory without a dependency on a running TM1 Server.

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

Installation
------------

.. code:: sh

   pip install tm1filetools

Example Usage
-------------

.. code:: python

   from pathlib import Path
   from tm1filetools import TM1FileTool

   path = Path("./data")

   ft = TM1FileTool(path)

   orphans = ft.get_orphan_rules()

   ...

   ft.delete_all_blbs()

   ...

Running Tests
-------------

``$ pytest tests
``
