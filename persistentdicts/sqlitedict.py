# -*- coding: utf-8 -*-

from __future__ import with_statement
import collections
import proxydict
import sqlite


class SqliteStringDict(collections.MutableMapping):
    """
    KyotoCabinet database with an interface of dictionary
    """

    def __init__(self, path, table="dict"):
        self.path = path
        self.table = table
        self.conn = sqlite3.connect(self.path)

    def __len__(self):
        pass

    def __getitem__(self, key):
        pass

    def __setitem__(self, key, value):
        pass

    def __delitem__(self, key):
        pass

    def __contains__(self, key):
        pass

    def iteritems(self):
        pass

    def __iter__(self):
        pass


class SqliteDict(proxydict.JsonProxyDict):

    def __init__(self, path, *args, **kwargs):
        target = SqliteStringDict(path)
        super(proxydict.JsonProxyDict, self).__init__(target)
        self.update(dict(*args, **kwargs))
