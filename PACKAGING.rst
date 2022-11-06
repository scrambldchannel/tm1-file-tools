How to package
==============

Pretty rough so far, can be improved/automated.

Bump Version
------------

Bump version in ``src/tm1filetools/__init__.py`` e.g.:

.. code:: python

   """A package for working with files created by a TM1 database."""

   from .tools import TM1FileTool  # noqa

   __version__ = "0.3.2"  # noqa

Publish to PyPI
---------------

.. code:: sh

   flit build

.. _publish-to-pypi-1:

Publish to PyPI
---------------

.. code:: sh

   flit publish
