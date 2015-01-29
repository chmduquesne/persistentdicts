persistentdicts
===============

|Build Status| |Coverage Status| |License|

dict-like interfaces for various databases

Key differences with competing projects
=======================================

If you search on pypi, you will find a few competing projects: pdicts,
durabledicts, etc. The key differences between persistentdicts and those
are:

-  Implementations of persistentdicts do not keep a local cache
   dictionary: changes are immediately written to database. Iterators
   are also proceeding directly on the database. It allows to interact
   with datasets that would not fit in RAM otherwise.

-  The test suite is significantly bigger than in all the other
   implementation I have seen. When relevant, tests have been backported
   from the CPython test suite of dict.

-  Serialization is done in json rather than using pickle.

Gotchas
-------

You can't modify a value of the dictionary in place. For example:

::

    >>> import persistentdicts

    >>> d = persistentdicts.SqliteDict()
    >>> d["a"] = []
    >>> d["a"].append(1)

    >>> d["a"] # with a normal dict, you would get [1]
    []

That is because ``d["a"]`` returns a copy of the database entry for the
key ``"a"``, and not a reference to a python object. Modifying this copy
(with ``append``) does not affect the database itself.

To circumvent this, you should do:

::

    >>> import persistentdicts

    >>> d = persistentdicts.SqliteDict()
    >>> d["a"] = []
    >>> d["a"] = d["a"] + [1]

    >>> d["a"]
    [1]

Similarly, ``setdefault`` will not work as expected since it does not
return a reference to the stored value, but a copy of this value.

::

    >>> import persistentdicts

    >>> d = persistentdicts.SqliteDict()
    >>> d.setdefault("a", []).append(1)

    >>> d["a"]
    []

Databases supported so far
--------------------------

Done:

-  kyotocabinet
-  sqlite
-  cassandra

Planned:

-  leveldb
-  redis
-  memcachedb
-  lightcloud

You can request new formats on the `bug tracker <https://github.com/chmduquesne/persistentdicts/issues>`__.

Short documentation
===================

persistentdicts.sqlitedict.SqliteDict
-------------------------------------

::

    persistentdicts.sqlitedict.SqliteDict(path=":memory:", table="dict", isolation_level="DEFERRED", *args, **kwargs)

-  ``path`` is the path to the file where you wish to store the data
-  ``dict`` is the table to use in this file
-  ``isolation_level`` is the isolation level used for all transactions.
   See the `sqlite
   documentation <https://docs.python.org/2/library/sqlite3.html#sqlite3.Connection.isolation_level>`__
   for more details.
-  the remaining arguments ``*args, **kwargs`` are used to fill the
   dictionary (like a normal ``dict``)

persistentdicts.kyotocabinetdict.KyotoCabinetDict
-------------------------------------------------

::

    persistentdicts.kyotocabinetdict.KyotoCabinetDict(path, *args, **kwargs)

-  ``path`` is the path to the file where you wish to store the data.
   The file extension matters and will determine which format is going
   to be used internally (must be one of .kch, .kct, .kcd, .kcf or
   .kcx). See the `kyotocabinet
   documentation <http://fallabs.com/kyotocabinet/pythonlegacydoc/kyotocabinet.DB-class.html#open>`__
   for more details.
-  the remaining arguments ``*args, **kwargs`` are used to fill the
   dictionary (like a normal ``dict``)

persistentdicts.cassandradict.CassandraDict
-------------------------------------------

::

    persistentdicts.cassandradict.CassandraDict(contact_points=("127.0.0.1",), port=9042, keyspace="dict", table="dict", *args, **kwargs)

-  ``contact_points`` is an initial list of ip addresses which are part of
   the Cassandra cluster. The Cassandra driver will automatically discover
   the rest of the cluster.
-  ``port`` is the port on which Cassandra runs.
-  ``keyspace`` is the keyspace used to store the data. This keyspace will
   be deleted if the method ``.delete()`` is called on the CassandraDict
-  ``table`` is the name of the table used to store the data.
-  the remaining arguments ``*args, **kwargs`` are used to fill the
   dictionary (like a normal ``dict``)

.. |Build Status| image:: https://travis-ci.org/chmduquesne/persistentdicts.svg
   :target: https://travis-ci.org/chmduquesne/persistentdicts
.. |Coverage Status| image:: https://coveralls.io/repos/chmduquesne/persistentdicts/badge.svg?branch=master
   :target: https://coveralls.io/r/chmduquesne/persistentdicts?branch=master
.. |License| image:: https://pypip.in/license/persistentdicts/badge.svg?style=flat
   :target: https://pypi.python.org/pypi/persistentdicts/
