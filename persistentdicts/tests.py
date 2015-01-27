# -*- coding: utf-8 -*-
import persistentdicts
import unittest
import tempfile
import os


class DictionaryTestCase():
    """
    Generic dictionary test case, used to test the serializeddicts
    """

    def setUp(self):
        raise NotImplementedError

    def tearDown(self):
        raise NotImplementedError

    def get_dictionary(self):
        raise NotImplementedError

    def test_create(self):
        d = self.get_dictionary()
        self.assertEqual(dict(d), {})
        self.assertEqual(list(d), [])
        self.assertEqual(len(d), 0)

    def test_empty(self):
        d = self.get_dictionary()   # tested
        m = dict()                  # mirror
        self.assertEqual(dict(d), m)

    def test_len(self):
        d = self.get_dictionary()   # tested
        m = dict()                  # mirror
        self.assertEqual(len(d), 0)
        elems = ["a", 1, None]
        for e in elems:
            d[e] = e
            m[e] = e
        self.assertEqual(len(d), len(elems))
        self.assertEqual(dict(d), m)

    def test_len_deleted_element(self):
        d = self.get_dictionary()
        self.assertEqual(len(d), 0)
        elems = range(1000)
        for e in elems:
            d[e] = e
        self.assertEqual(len(d), len(elems))
        del d[elems[0]]
        self.assertEqual(len(d), len(elems) - 1)

    def test_getitem_empty(self):
        d = self.get_dictionary()
        with self.assertRaises(KeyError):
            d["does not exist"]

    def test_getitem_assign(self):
        d = self.get_dictionary()
        elems = ["a", 1, None]
        for e in elems:
            d[e] = e
        for e in elems:
            self.assertEqual(d[e], e)

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

    def test_in(self):
        d = self.get_dictionary()
        self.assertEqual("a" in d, False)
        d["a"] = "a"
        self.assertEqual("a" in d, True)

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
        d.clear()
        self.assertEqual(len(d), 0)

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

    def test_has_key(self):
        d = self.get_dictionary()
        self.assertEqual(d.has_key("a"), False)
        d["a"] = "a"
        self.assertEqual(d.has_key("a"), True)

    def test_items(self):
        d = self.get_dictionary()
        elems = ["a", 1, None]
        for e in elems:
            d[e] = e
        for key, value in d.items():
            self.assertEqual(key, value)

    def test_iteritems(self):
        d = self.get_dictionary()
        elems = ["a", 1, None]
        for e in elems:
            d[e] = e
        for key, value in d.iteritems():
            self.assertEqual(key, value)

    def test_iterkeys(self):
        d = self.get_dictionary()
        elems = ["a", 1, None]
        for e in elems:
            d[e] = e
        for key in d.iterkeys():
            self.assertEqual(d[key], key)

    def test_itervalues(self):
        d = self.get_dictionary()
        elems = ["a", 1, None]
        for e in elems:
            d[e] = e
        for value in d.itervalues():
            self.assertEqual(d[value], value)

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
        return persistentdicts.ProxyDict()


class JsonProxyDictTestCase(DictionaryTestCase, unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def get_dictionary(self):
        return persistentdicts.JsonProxyDict()


class KyotoCabinetDictTestCase(DictionaryTestCase, unittest.TestCase):

    def setUp(self):
        fd, path = tempfile.mkstemp(suffix='.kch')
        os.close(fd)
        os.unlink(path)
        self.path = path

    def tearDown(self):
        os.unlink(self.path)

    def get_dictionary(self):
        return persistentdicts.KyotoCabinetDict(self.path)


class SqliteDictTestCase(DictionaryTestCase, unittest.TestCase):

    def setUp(self):
        fd, path = tempfile.mkstemp(suffix='.db')
        os.close(fd)
        os.unlink(path)
        self.path = path

    def tearDown(self):
        os.unlink(self.path)

    def get_dictionary(self):
        return persistentdicts.SqliteDict(self.path)
