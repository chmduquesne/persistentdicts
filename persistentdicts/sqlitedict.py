# -*- coding: utf-8 -*-

from __future__ import with_statement
import collections
import proxydict
import sqlite3
import contextlib


class SqliteStringDict(collections.MutableMapping):
    """
    Sqlite database with an interface of dictionary
    """

    def __init__(self, path, table="dict"):
        self.path = path
        self.table = table
        self.conn = sqlite3.connect(self.path)

        with contextlib.closing(self.conn.cursor()) as c:
            c.execute("CREATE TABLE IF NOT EXISTS %s "
                      "(key TEXT PRIMARY KEY, value TEXT)" % self.table)
            self.conn.commit()

    def __len__(self):
        with contextlib.closing(self.conn.cursor()) as c:
            c.execute("SELECT COUNT(*) from %s" % self.table)
            res = int(c.fetchone()[0])
        return res

    def __getitem__(self, key):
        with contextlib.closing(self.conn.cursor()) as c:
            c.execute("SELECT value FROM %s "
                      "WHERE key = ? LIMIT 1" % self.table,
                      (key,))
            row = c.fetchone()
            if row is None:
                raise KeyError
            return row[0]

    def __setitem__(self, key, value):
        with contextlib.closing(self.conn.cursor()) as c:
            c.execute("INSERT OR REPLACE INTO %s (key, value)"
                      "VALUES (?, ?)" % self.table, (key, value))
            self.conn.commit()

    def __delitem__(self, key):
        if key not in self:
            raise KeyError
        with contextlib.closing(self.conn.cursor()) as c:
            c.execute("DELETE FROM %s "
                      "WHERE key=?" % self.table,
                      (key,))
            self.conn.commit()

    def __contains__(self, key):
        with contextlib.closing(self.conn.cursor()) as c:
            c.execute("SELECT 1 FROM %s "
                      "WHERE key=? LIMIT 1" % self.table,
                      (key,))
            row = c.fetchone()
            return row is not None

    def iteritems(self):
        with contextlib.closing(self.conn.cursor()) as c:
            for row in c.execute(
                    "SELECT key, value FROM %s" % self.table):
                yield row[0], row[1]

    def __iter__(self):
        for key, value in self.iteritems():
            yield key


class SqliteDict(proxydict.JsonProxyDict):

    def __init__(self, path, *args, **kwargs):
        target = SqliteStringDict(path)
        super(proxydict.JsonProxyDict, self).__init__(target)
        self.update(dict(*args, **kwargs))
