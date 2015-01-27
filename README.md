# persistentdicts

[![Build Status](https://travis-ci.org/chmduquesne/persistentdicts.svg)](https://travis-ci.org/chmduquesne/persistentdicts)
[![Coverage Status](https://coveralls.io/repos/chmduquesne/persistentdicts/badge.svg?branch=master)](https://coveralls.io/r/chmduquesne/persistentdicts?branch=master)
[![License](https://pypip.in/license/persistentdicts/badge.svg?style=flat)](https://pypi.python.org/pypi/persistentdicts/)

This python library exposes various databases through dict-like objects.

Key difference with competing projects
======================================

If you search on pypi, you will find a few competing projects: pdicts,
durabledicts, etc. The key differences between persistentdicts and those
are:

- Implementations of persistentdicts do not keep a local cache dictionary:
  changes are immediately written to database. Iterators are also
  proceeding directly on the database. It allows to interact with datasets
  that would not fit in RAM otherwise.

- The test suite is significantly bigger than in all the other
  implementation I have seen. When relevant, tests have been backported
  from the CPython test suite of dict.

- Serialization is done in json rather than using pickle.

Gotchas
-------

You can't modify a value of the dictionary in place. For example:

    >>> import persistentdicts
    
    >>> d = persistentdicts.SqliteDict()
    >>> d["a"] = []
    >>> d["a"].append(1)
    
    >>> d["a"] # with a normal dict, you would get [1]
    []

That is because `d["a"]` returns a copy of the database entry for the key
`"a"`, and not a reference to a python object. Modifying this copy (with
`append`) does not affect the database itself.

To circumvent this, you should do:

    >>> import persistentdicts
    
    >>> d = persistentdicts.SqliteDict()
    >>> d["a"] = []
    >>> d["a"] = d["a"] + [1]
    
    >>> d["a"]
    [1]

Similarly, `setdefault` will not work as expected since it does not return
a reference to the stored value, but a copy of this value.

    >>> import persistentdicts
    
    >>> d = persistentdicts.SqliteDict()
    >>> d.setdefault("a", []).append(1)
    
    >>> d["a"]
    []

Databases supported so far
--------------------------

Done:

* sqlite
* kyotocabinet

Planned:

* cassandra
* leveldb

You can request new formats on the bug tracker.

Short documentation
===================

persistentdicts.SqliteDict
--------------------------

    Sqlitedict(path=":memory:", table="dict", isolation_level="DEFERRED", *args, **kwargs)

  * `path` is the path to the file where you wish to store the data
  * `dict` is the table to use in this file
  * `isolation_level` is the isolation level used for all transactions.
    See the [sqlite documentation][1] for more details.
  * the remaining arguments `*args, **kwargs` are used to fill the
    dictionary (like a normal `dict`)

persistentdicts.KyotoCabinetDict
--------------------------------

    Sqlitedict(path, *args, **kwargs)

  * `path` is the path to the file where you wish to store the data. The
    file extension matters and will determine which format is going to be
    used internally (must be one of .kch, .kct, .kcd, .kcf or .kcx). See
    the [kyotocabinet documentation][2] for more details.
  * the remaining arguments `*args, **kwargs` are used to fill the
    dictionary (like a normal `dict`)

[1]: https://docs.python.org/2/library/sqlite3.html#sqlite3.Connection.isolation_level
[2]: http://fallabs.com/kyotocabinet/pythonlegacydoc/kyotocabinet.DB-class.html#open
