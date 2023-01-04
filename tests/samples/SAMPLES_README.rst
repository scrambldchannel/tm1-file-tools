Samples for Testing
===================

config_files
------------

A few different samples of cfg files (e.g. valid, invalid)

json_out
--------

Examples of valid json representations of tm1 objects that can be used to instantiate TM1py

server
------

An example directory structure.

* cfg - contains a config file with relative paths to the data and log dirs
* data - base folder for cube, dim, pro files etc
    * dim}subs folders for public subsets per dim
    * cub}vues folders for public views per cube
    * user1/user2 - example user folders that can contain private views and subsets in nested }subs / }vues folders
* export - an arbitrary folder for dumping cma files into
* logs - all logging files