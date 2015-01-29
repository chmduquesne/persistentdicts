# -*- coding: utf-8 -*-

from __future__ import with_statement
from . import proxydict
import collections
import cassandra
import cassandra.cluster


class CassandraStringDict(collections.MutableMapping):
    """
    Sqlite database with an interface of dictionary
    """

    def __init__(self, contact_points, port, keyspace, table):
        self.contact_points = contact_points
        self.port = port
        self.cluster = cassandra.cluster.Cluster(contact_points, port)
        self.keyspace = keyspace
        self.table = table
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
        self.session.execute(
                "CREATE TABLE IF NOT EXISTS %s "
                "(key text PRIMARY KEY, value text)"
                % self.table)

    def delete(self):
            self.session.execute("DROP KEYSPACE %s" % self.keyspace)
            self.session.shutdown()

    def __len__(self):
        rows = self.session.execute(
                "SELECT COUNT(*) FROM %s " % self.table
                )
        for row in rows:
            return row[0]

    def __getitem__(self, key):
        rows = self.session.execute(
                "SELECT key, value FROM %s " % self.table +
                "WHERE key = %s LIMIT 1", (key,)
                )
        for key, value in rows:
            return value
        raise KeyError

    def __setitem__(self, key, value):
        self.session.execute(
                "INSERT INTO %s (key, value)" % self.table +
                "VALUES (%s, %s)", (key, value))

    def __delitem__(self, key):
        if key not in self:
            raise KeyError
        self.session.execute(
                "DELETE FROM %s " % self.table +
                "WHERE key = %s", (key,))

    def __contains__(self, key):
        res = False
        rows = self.session.execute(
                "SELECT * FROM %s " % self.table +
                "WHERE key = %s LIMIT 1", (key,))
        for row in rows:
            res = True
        return res

    def iteritems(self):
        rows = self.session.execute(
                "SELECT key, value FROM %s " % self.table
                )
        for key, value in rows:
            yield key, value

    def __iter__(self):
        for key, value in self.iteritems():
            yield key


class CassandraDict(proxydict.JsonProxyDict):

    def __init__(self, contact_points=("127.0.0.1",), port=9042,
            keyspace="dict", table="dict", *args, **kwargs):
        target = CassandraStringDict(contact_points, port, keyspace, table)
        super(proxydict.JsonProxyDict, self).__init__(target)
        self.update(dict(*args, **kwargs))

    def copy(self):
        t = self.target
        return CassandraDict(t.contact_points, t.port, t.keyspace, t.table)

    def delete(self):
        return self.target.delete()
