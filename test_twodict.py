#!/usr/bin/env python

"""Contains tests for the twodict module."""

import sys
import unittest

try:
    from twodict import TwoWayOrderedDict
except ImportError as error:
    print(error)
    sys.exit(1)

# Lambda to make a call to the parent of the given object
super_call = lambda obj, method: getattr(super(obj.__class__, obj), method)()


class TestInit(unittest.TestCase):

    """Test case for the TwoWayOrderedDict initialization."""

    def test_init_ordered(self):
        tdict = TwoWayOrderedDict([('a', 1), ('b', 2), ('c', 3)])
        self.assertEqual(tdict.items(), [('a', 1), ('b', 2), ('c', 3)])

    def test_init_unordered_kwargs(self):
        tdict = TwoWayOrderedDict(a=1, b=2, c=3)
        self.assertEqual(tdict.items(), [('a', 1), ('c', 3), ('b', 2)])

    def test_init_unordered_dict(self):
        tdict = TwoWayOrderedDict({'a': 1, 'b': 2, 'c': 3})
        self.assertEqual(tdict.items(), [('a', 1), ('c', 3), ('b', 2)])


class TestGetItem(unittest.TestCase):

    """Test case for the TwoWayOrderedDict __getitem__ method."""

    def setUp(self):
        self.tdict = TwoWayOrderedDict(a=1, b=2, c=3)

    def test_get_item_by_key(self):
        self.assertEqual(self.tdict['a'], 1)

    def test_get_item_by_value(self):
        self.assertEqual(self.tdict[1], 'a')

    def test_get_item_not_exist(self):
        self.assertRaises(KeyError, self.tdict.__getitem__, 'd')


class TestSetItem(unittest.TestCase):

    """Test case for the TwoWayOrderedDict __setitem__ method."""

    def setUp(self):
        self.tdict = TwoWayOrderedDict(a=1, b=2)

    def test_set_item(self):
        self.tdict['c'] = 3
        self.assertEqual(self.tdict.items(), [('a', 1), ('b', 2), ('c', 3)])

    def test_set_item_already_in_dict(self):
        self.tdict['a'] = 10
        self.assertEqual(self.tdict.items(), [('a', 10), ('b', 2)])

    def test_set_item_overwrite_value_as_key(self):
        self.tdict[1] = 'a'
        self.assertEqual(self.tdict.items(), [('b', 2), (1, 'a')])

    def test_set_item_overwrite_use_value_with_new_key(self):
        self.tdict['c'] = 1
        self.assertEqual(self.tdict.items(), [('b', 2), ('c', 1)])

    def test_set_item_key_equals_value(self):
        self.tdict['c'] = 'c'
        self.assertEqual(self.tdict.items(), [('a', 1), ('b', 2), ('c', 'c')])

        self.tdict['d'] = 4
        self.assertEqual(self.tdict.items(), [('a', 1), ('b', 2), ('c', 'c'), ('d', 4)])

    def test_set_item_overwrite_advanced(self):
        tdict = TwoWayOrderedDict([('a', 1), ('b', 2), ('c', 'c'), ('d', 4)])

        tdict['c'] = 3
        self.assertEqual(tdict.items(), [('a', 1), ('b', 2), ('c', 3), ('d', 4)])

        tdict['c'] = 1
        self.assertEqual(tdict.items(), [('b', 2), ('c', 1), ('d', 4)])

        tdict['c'] = 'b'
        self.assertEqual(tdict.items(), [('c', 'b'), ('d', 4)])

        self.assertEqual(super_call(tdict, "__repr__"), "{'b': 'c', 4: 'd', 'd': 4, 'c': 'b'}")


class TestDelItem(unittest.TestCase):

    """Test case for the TwoWayOrderedDict __delitem__ method."""

    def setUp(self):
        self.tdict = TwoWayOrderedDict([('a', 1), ('b', 'b'), ('c', 3)])

    def test_del_item_by_key(self):
        del self.tdict['a']
        self.assertEqual(self.tdict.items(), [('b', 'b'), ('c', 3)])

    def test_del_item_by_value(self):
        del self.tdict[3]
        self.assertEqual(self.tdict.items(), [('a', 1), ('b', 'b')])

    def test_del_item_not_exist(self):
        self.assertRaises(KeyError, self.tdict.__delitem__, 'd')

    def test_del_item_key_equals_value(self):
        del self.tdict['b']
        self.assertEqual(self.tdict.items(), [('a', 1), ('c', 3)])


class TestLength(unittest.TestCase):

    """Test case for the TwoWayOrderedDict __len__ method."""

    def test_length_empty(self):
        tdict = TwoWayOrderedDict()
        self.assertEqual(len(tdict), 0)

    def test_length_not_empty(self):
        tdict = TwoWayOrderedDict(a=1, b=2, c=3)
        self.assertEqual(len(tdict), 3)


class TestIteration(unittest.TestCase):

    """Test case for the TwoWayOrderedDict __iter__ & __reversed__  methods."""

    KEY_INDEX = 0

    def setUp(self):
        self.items = [('a', 1), ('b', 2), ('c', 3)]
        self.tdict = TwoWayOrderedDict(self.items)

    def test_iter(self):
        for index, key in enumerate(self.tdict):
            self.assertEqual(key, self.items[index][self.KEY_INDEX])

    def test_iter_reversed(self):
        for index, key in enumerate(reversed(self.tdict)):
            reversed_index = (index + 1) * (-1)
            self.assertEqual(key, self.items[reversed_index][self.KEY_INDEX])


class TestComparison(unittest.TestCase):

    """Test case for the TwoWayOrderedDict compare methods."""

    def test_equal(self):
        t1 = TwoWayOrderedDict(a=1, b=2, c=3)
        t2 = TwoWayOrderedDict(a=1, b=2, c=3)

        self.assertEqual(t1, t2)

    def test_not_equal(self):
        t1 = TwoWayOrderedDict(a=1, b=2, c=3)
        t2 = TwoWayOrderedDict(a=1, b=2, d=3)

        self.assertNotEqual(t1, t2)


class TestGetValuesAndKeys(unittest.TestCase):

    """Test case for the TwoWayOrderedDict values() & keys() methods."""

    def setUp(self):
        self.tdict_empty = TwoWayOrderedDict()
        self.tdict_not_empty = TwoWayOrderedDict([('a', 1), ('b', 2), ('c', 3)])

    def test_get_keys_empty(self):
        self.assertEqual(self.tdict_empty.keys(), [])

    def test_get_keys_not_empty(self):
        self.assertEqual(self.tdict_not_empty.keys(), ['a', 'b', 'c'])

    def test_get_values_empty(self):
        self.assertEqual(self.tdict_empty.values(), [])

    def test_get_values_not_empty(self):
        self.assertEqual(self.tdict_not_empty.values(), [1, 2, 3])


class TestPopMethods(unittest.TestCase):

    """Test case for the TwoWayOrderedDict pop() & popitem() methods."""

    def setUp(self):
        self.tdict = TwoWayOrderedDict([('a', 1), ('b', 2), ('c', 3)])

    def test_pop_by_key(self):
        self.assertEqual(self.tdict.pop('a'), 1)

    def test_pop_by_value(self):
        self.assertEqual(self.tdict.pop(1), 'a')

    def test_pop_raises(self):
        self.assertRaises(KeyError, self.tdict.pop, 'd')

    def test_pop_with_default_value(self):
        self.assertIsNone(self.tdict.pop('d', None))
        self.assertEqual(self.tdict.pop('d', 10), 10)

    def test_popitem_last(self):
        self.assertEqual(self.tdict.popitem(), ('c', 3))

    def test_popitem_first(self):
        self.assertEqual(self.tdict.popitem(last=False), ('a', 1))

    def test_popitem_raises(self):
        for _ in range(len(self.tdict)): self.tdict.popitem()
        self.assertRaises(KeyError, self.tdict.popitem)


class TestUpdate(unittest.TestCase):

    """Test case for the TwoWayOrderedDict update method."""

    def setUp(self):
        self.tdict = TwoWayOrderedDict([('a', 1), ('b', 2)])

    def test_update_ordered(self):
        self.tdict.update([('a', 10), ('c', 3), ('d', 4), ('e', 5)])
        self.assertEqual(self.tdict.items(), [('a', 10), ('b', 2), ('c', 3), ('d', 4), ('e', 5)])

    def test_update_unordered(self):
        self.tdict.update({'a': 10, 'c': 3, 'd': 4, 'e': 5})
        self.assertEqual(self.tdict.items(), [('a', 10), ('b', 2), ('c', 3), ('e', 5), ('d', 4)])


class TestSetDefault(unittest.TestCase):

    """Test case for the TwoWayOrderedDict setdefault method."""

    def setUp(self):
        self.tdict = TwoWayOrderedDict([('a', 1), ('b', 2)])

    def test_setdefault_by_key(self):
        self.assertEqual(self.tdict.setdefault('a'), 1)

    def test_setdefault_by_value(self):
        self.assertEqual(self.tdict.setdefault(1), 'a')

    def test_setdefault_not_exist(self):
        self.assertIsNone(self.tdict.setdefault('c'))
        self.assertEqual(self.tdict.setdefault('d', 'd'), 'd')

        self.assertEqual(self.tdict.items(), [('a', 1), ('b', 2), ('c', None), ('d', 'd')])


class TestCopy(unittest.TestCase):

    """Test case for the TwoWayOrderedDict copy method."""

    def test_copy(self):
        tdict = TwoWayOrderedDict([('a', 1), ('b', 2)])

        tdict_copy = tdict.copy()
        self.assertEqual(tdict, tdict_copy)

        tdict_copy['c'] = 3
        self.assertNotEqual(tdict, tdict_copy)


class TestClear(unittest.TestCase):

    """Test case for the TwoWayOrderedDict clear method."""

    def test_clear_empty(self):
        tdict = TwoWayOrderedDict()
        tdict.clear()
        self.assertEqual(len(tdict), 0)

    def test_clear_not_empty(self):
        tdict = TwoWayOrderedDict(a=1, b=2, c=3)
        tdict.clear()
        self.assertEqual(len(tdict), 0)


def main():
    unittest.main()


if __name__ == "__main__":
    main()
