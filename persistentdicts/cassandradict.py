# -*- coding: utf-8 -*-

from __future__ import with_statement
import collections
import proxydict
import cassandra


class CassandraStringDict(collections.MutableMapping):
    """
    Sqlite database with an interface of dictionary
    """

    def __init__(self, contact_points=("127.0.0.1",), port=9042,
            keyspace="dict"):
        self.contact_points = contact_points
        self.port = port
        self.cluster = cassandra.cluster.Cluster(contact_points, ports)
        self.keyspace = keyspace
        try:
            self.session = self.cluster.connect(self.keyspace)
        except cassandra.InvalidRequest:
            self.session = self.cluster.connect()
            self.session.execute(
                    "CREATE KEYSPACE %s "
                    "WITH REPLICATION = "
                    "{'class': 'SimpleStrategy', "
                    "'replication_factor': 3}" % self.keyspace
                    )
            self.session.set_keyspace(self.keyspace)

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


class CassandraDict(proxydict.JsonProxyDict):

    def __init__(self, path=":memory:", table="dict",
                 isolation_level="DEFERRED", *args, **kwargs):
        target = SqliteStringDict(path, table=table,
                                  isolation_level=isolation_level)
        super(proxydict.JsonProxyDict, self).__init__(target)
        self.update(dict(*args, **kwargs))

    def copy(self):
        t = self.target
        return SqliteDict(t.path, t.table, t.isolation_level)
