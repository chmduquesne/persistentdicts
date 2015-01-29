# -*- coding: utf-8 -*-
import persistentdicts
import unittest
import tempfile
import os
import sys
from . import proxydict
from . import sqlitedict
from . import kyotocabinetdict
from . import cassandradict


class DictionaryTestCase():
    """
    Generic dictionary test case

    Some tests are "stolen" from the standard lib
    https://github.com/python/cpython/blob/master/Lib/test/test_dict.py
    """

    def setUp(self):
        raise NotImplementedError

    def tearDown(self):
        raise NotImplementedError

    def get_dictionary(self):
        raise NotImplementedError

    def assertInSyncWithCopy(self, d):
        return self.assertEqual(dict(d), dict(d.copy()))

    def test_create(self):
        d = self.get_dictionary()
        self.assertEqual(dict(d), {})
        self.assertEqual(list(d), [])
        self.assertEqual(len(d), 0)

    def test_empty(self):
        d = self.get_dictionary()
        self.assertEqual(dict(d), {})
        self.assertInSyncWithCopy(d)

    def test_len(self):
        d = self.get_dictionary()
        self.assertEqual(len(d), 0)
        elems = ["a", 1, None]
        for e in elems:
            d[e] = e
        self.assertEqual(len(d), len(elems))
        self.assertInSyncWithCopy(d)

    def test_len_deleted_element(self):
        d = self.get_dictionary()
        self.assertEqual(len(d), 0)
        elems = range(100)
        for e in elems:
            d[e] = e
        self.assertEqual(len(d), len(elems))
        self.assertInSyncWithCopy(d)
        del d[elems[0]]
        self.assertEqual(len(d), len(elems) - 1)
        self.assertInSyncWithCopy(d)

    def test_getitem_empty(self):
        d = self.get_dictionary()
        with self.assertRaises(KeyError):
            d["does not exist"]

    def test_setitem(self):
        d = self.get_dictionary()
        elems = ["a", 1, None]
        for e in elems:
            d[e] = e
        for e in elems:
            self.assertEqual(d[e], e)
        self.assertInSyncWithCopy(d)

    def test_delete_empty(self):
        d = self.get_dictionary()
        with self.assertRaises(KeyError):
            del d["does not exist"]

    def test_delete(self):
        d = self.get_dictionary()
        d["a"] = "a"
        self.assertEqual(d["a"], "a")
        del d["a"]
        with self.assertRaises(KeyError):
            del d["a"]
        self.assertInSyncWithCopy(d)

    def test_in(self):
        d = self.get_dictionary()
        self.assertEqual("a" in d, False)
        d["a"] = "a"
        self.assertEqual("a" in d, True)
        self.assertInSyncWithCopy(d)

    def test_not_in(self):
        d = self.get_dictionary()
        self.assertEqual("a" not in d, True)
        d["a"] = "a"
        self.assertEqual("a" not in d, False)

    def test_iter(self):
        d = self.get_dictionary()
        elems = ["a", 1, None]
        for e in elems:
            d[e] = e
        for e in iter(d):
            self.assertEqual(d[e], e)

    def test_iter_for_in(self):
        d = self.get_dictionary()
        elems = ["a", 1, None]
        for e in elems:
            d[e] = e
        for e in d:
            self.assertEqual(d[e], e)

    def test_clear(self):
        d = self.get_dictionary()
        elems = ["a", 1, None]
        for e in elems:
            d[e] = e
        self.assertEqual(len(d), 3)
        self.assertInSyncWithCopy(d)
        d.clear()
        self.assertEqual(len(d), 0)
        self.assertInSyncWithCopy(d)

    def test_get_empty(self):
        d = self.get_dictionary()
        res = d.get("does not exist")
        self.assertEqual(res, None)

    def test_get_default(self):
        d = self.get_dictionary()
        res = d.get("does not exist", "default value")
        self.assertEqual(res, "default value")

    def test_get(self):
        d = self.get_dictionary()
        elems = ["a", 1, None]
        for e in elems:
            d[e] = e
        for e in d:
            self.assertEqual(d.get(e), e)

    def test_items(self):
        d = self.get_dictionary()
        elems = ["a", 1, None]
        for e in elems:
            d[e] = e
        for key, value in d.items():
            self.assertEqual(key, value)

    # irrelevant in python3

    #def test_has_key(self):
    #    d = self.get_dictionary()
    #    self.assertEqual(d.has_key("a"), False)
    #    d["a"] = "a"
    #    self.assertEqual(d.has_key("a"), True)

    #def test_iteritems(self):
    #    d = self.get_dictionary()
    #    elems = ["a", 1, None]
    #    for e in elems:
    #        d[e] = e
    #    for key, value in d.iteritems():
    #        self.assertEqual(key, value)

    #def test_iterkeys(self):
    #    d = self.get_dictionary()
    #    elems = ["a", 1, None]
    #    for e in elems:
    #        d[e] = e
    #    for key in d.iterkeys():
    #        self.assertEqual(d[key], key)

    #def test_itervalues(self):
    #    d = self.get_dictionary()
    #    elems = ["a", 1, None]
    #    for e in elems:
    #        d[e] = e
    #    for value in d.itervalues():
    #        self.assertEqual(d[value], value)

    def test_keys(self):
        d = self.get_dictionary()
        elems = ["a", 1, None]
        for e in elems:
            d[e] = e
        for key in d.keys():
            self.assertEqual(d[key], key)

    def test_pop_empty(self):
        d = self.get_dictionary()
        with self.assertRaises(KeyError):
            res = d.pop("does not exist")

    def test_pop_default(self):
        d = self.get_dictionary()
        res = d.pop("does not exist", "default value")
        self.assertEqual(res, "default value")

    def test_pop(self):
        d = self.get_dictionary()
        d["a"] = "a"
        res = d.pop("a")
        self.assertEqual(res, "a")

    def test_values(self):
        d = self.get_dictionary()
        elems = ["a", 1, None]
        for e in elems:
            d[e] = e
        for value in d.values():
            self.assertEqual(d[value], value)

    def test_update(self):
        update_from = dict()
        elems = ["a", 1, None]
        for e in elems:
            update_from[e] = e
        d = self.get_dictionary()
        d.update(update_from)
        self.assertEqual(dict(d), update_from)

    def test_constructor(self):
        # Modified from standard lib
        d = self.get_dictionary()
        self.assertEqual(d, {})
        self.assertIsNot(d, {})

    def test_bool(self):
        # Modified from standard lib
        d = self.get_dictionary()
        self.assertIs(not d, True)
        self.assertIs(bool(d), False)
        d.update({1: 2})
        self.assertTrue(d)
        self.assertIs(bool(d), True)

    def test_copy(self):
        # Modified from standard lib
        d = self.get_dictionary()
        d.update({1: 1, 2: 2, 3: 3})
        self.assertEqual(d.copy(), {1: 1, 2: 2, 3: 3})
        self.assertEqual({}.copy(), {})
        self.assertRaises(TypeError, d.copy, None)

    def test_str(self):
        # Modified from standard lib
        d = self.get_dictionary()
        self.assertEqual(str(d), '{}')
        d[1] = 2
        self.assertEqual(str(d), '{1: 2}')
        d = {}
        d[1] = d
        self.assertEqual(str(d), '{1: {...}}')

    # These test still fail

    # def test_invalid_keyword_arguments(self):
    #     """
    #     Modified from standard lib
    #     """
    #     class Custom(dict):
    #         pass
    #     for invalid in {1 : 2}, Custom({1 : 2}):
    #         with self.assertRaises(TypeError):
    #             d = self.get_dictionary()
    #             d.update(**invalid)

    # def test_mutating_iteration(self):
    #     # Modified from standard lib
    #     # changing dict size during iteration
    #     d = self.get_dictionary()
    #     d[1] = 1
    #     with self.assertRaises(RuntimeError):
    #         for i in d:
    #             d[i+1] = 1


class RealDictTestCase(DictionaryTestCase, unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def get_dictionary(self):
        return dict()


class ProxyDictTestCase(DictionaryTestCase, unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def get_dictionary(self):
        return proxydict.ProxyDict()


class JsonProxyDictTestCase(DictionaryTestCase, unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def get_dictionary(self):
        return proxydict.JsonProxyDict()


class KyotoCabinetDictTestCase(DictionaryTestCase, unittest.TestCase):

    def setUp(self):
        fd, path = tempfile.mkstemp(suffix='.kch')
        os.close(fd)
        os.unlink(path)
        self.path = path

    def tearDown(self):
        os.unlink(self.path)

    def get_dictionary(self):
        return kyotocabinetdict.KyotoCabinetDict(self.path)


class SqliteDictTestCase(DictionaryTestCase, unittest.TestCase):

    def setUp(self):
        fd, path = tempfile.mkstemp(suffix='.db')
        os.close(fd)
        os.unlink(path)
        self.path = path

    def tearDown(self):
        os.unlink(self.path)

    def get_dictionary(self):
        return sqlitedict.SqliteDict(self.path)


class CassandraDictTestCase(DictionaryTestCase, unittest.TestCase):

    def setUp(self):
        self.dictionary = cassandradict.CassandraDict()

    def tearDown(self):
        self.dictionary.delete()

    def get_dictionary(self):
        return self.dictionary
