
Quickstart
==========

Installation
------------

Install it using pip:

.. code-block:: console

   (.venv) $ pip install tm1filetools

Example Usage
-------------

The tool can be used to find, list and even cleanup the directory.

Initialise
^^^^^^^^^^

Pass a path object to the constructor:

.. code:: python

   from pathlib import Path
   from tm1filetools import TM1FileTool

   path = Path("./data")

   ft = TM1FileTool(path)

Listing Files
^^^^^^^^^^^^^

Get a list of all the non-control dim file objects:

.. code:: python

   dims = ft.get_dims()

Include the control dims too

.. code:: python

   dims = ft.get_dims(control=True)

Find *orphan* files (e.g. a ``.rux`` file without a corresponding ``.cub`` file):

.. code:: python

   orphans = ft.get_orphan_rules()

Deleting Files
^^^^^^^^^^^^^^

Deleting all *orphan* ``.rux`` files:

.. code:: python

   ft.delete_orphan_rules()


Deleting all ``.feeder`` files:

.. code:: python

   ft.delete_all_feeders()
