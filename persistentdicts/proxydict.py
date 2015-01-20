# -*- coding: utf-8 -*-
import collections
import json


class ProxyDict(collections.MutableMapping):

    def __init__(self, target=None, *args, **kwargs):
        if target is None:
            self.target = dict()
        else:
            self.target = target
        self.update(dict(*args, **kwargs))

    def __len__(self):
        return len(self.target)

    def __getitem__(self, key):
        return self.invert_trans(self.target[self.trans(key)])

    def __setitem__(self, key, value):
        self.target[self.trans(key)] = self.trans(value)

    def __delitem__(self, key):
        del self.target[self.trans(key)]

    def iteritems(self):
        for key, value in self.target.iteritems():
            yield self.invert_trans(key), self.invert_trans(value)

    def __iter__(self):
        for key, value in self.target.iteritems():
            yield self.invert_trans(key)

    def __str__(self):
        return str(dict(self))

    def has_key(self, key):
        return self.trans(key) in self.target

    def trans(self, x):
        return x

    def invert_trans(self, x):
        return x


class JsonProxyDict(ProxyDict):

    def trans(self, x):
        return json.dumps(x)

    def invert_trans(self, x):
        return json.loads(x)
