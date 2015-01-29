# -*- coding: utf-8 -*-

from __future__ import with_statement
from . import proxydict
from kyotocabinet import *
import collections


class DBOpen():
    """
    Allows to perform cleanly an operation on a KyotoCabinet database:

        >>> with DBOpen("example.kch") as db:
        >>>     print db.count()

    This will open the database before the operation, and close it after.
    """
    def __init__(self, path, mode=DB.OREADER):
        self.path = path
        self.db = None
        self.mode = mode

    def __enter__(self):
        self.db = DB()
        if not self.db.open(self.path, self.mode | DB.OCREATE):
            raise OSError(str(self.db.error()))
        return self.db

    def __exit__(self, type, value, traceback):
        if not self.db.close():
            raise OSError(str(self.db.error()))


class KyotoCabinetStringDict(collections.MutableMapping):
    """
    KyotoCabinet database with an interface of dictionary
    """

    def __init__(self, path):
        self.path = path
        with DBOpen(self.path, mode=DB.OWRITER) as db:
            pass

    def copy(self):
        return KyotoCabinetStringDict(path=self.path)

    def __len__(self):
        with DBOpen(self.path) as db:
            return int(db.count())

    def __getitem__(self, key):
        with DBOpen(self.path) as db:
            value = db.get_str(key)
            if value is None:
                raise KeyError(str(db.error()))
            return value

    def __setitem__(self, key, value):
        with DBOpen(self.path, mode=DB.OWRITER) as db:
            if not db.set(key, value):
                raise ValueError(str(db.error()))

    def __delitem__(self, key):
        with DBOpen(self.path, mode=DB.OWRITER) as db:
            if not db.remove(key):
                raise KeyError(str(db.error()))

    def __contains__(self, key):
        with DBOpen(self.path) as db:
            return db.check(key) != -1

    def iteritems(self):
        with DBOpen(self.path) as db:
            cursor = db.cursor()
            cursor.jump()
            while True:
                record = cursor.get_str(True)
                if not record:
                    break
                key = record[0]
                value = record[1]
                yield (key, value)
            cursor.disable()

    def __iter__(self):
        for key, value in self.iteritems():
            yield key


class KyotoCabinetDict(proxydict.JsonProxyDict):

    def __init__(self, path, *args, **kwargs):
        target = KyotoCabinetStringDict(path)
        super(proxydict.JsonProxyDict, self).__init__(target)
        self.update(dict(*args, **kwargs))

    def copy(self):
        t = self.target
        return KyotoCabinetDict(t.path)
