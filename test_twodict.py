#!/usr/bin/env python

"""Contains tests for the twodict module."""

import sys
import unittest

try:
    from twodict import (
        TwoWayOrderedDict,
        DictItemsView,
        DictValuesView,
        DictKeysView
    )
except ImportError as error:
    print(error)
    sys.exit(1)


########## Helpers ##########

class ExtraAssertions(object):

    MSG = "View: {0} is not equal to the given iterable"

    def assertViewEqualU(self, view, iterable):
        """Compare the given view with iterable. Order does NOT count."""
        view_list = list(view)

        for item in view_list:
            if item not in iterable:
                raise AssertionError(self.MSG.format(view_list))

    def assertViewEqualO(self, view, iterable):
        """Compare the given view with iterable. Order does count."""
        view_list = list(view)

        if view_list != iterable:
            raise AssertionError(self.MSG.format(view_list))

#############################


class TestInit(unittest.TestCase, ExtraAssertions):

    """Test case for the TwoWayOrderedDict initialization."""

    def test_init_ordered(self):
        tdict = TwoWayOrderedDict([('a', 1), ('b', 2), ('c', 3)])
        self.assertViewEqualO(tdict.items(), [('a', 1), ('b', 2), ('c', 3)])

    def test_init_unordered_kwargs(self):
        tdict = TwoWayOrderedDict(a=1, b=2, c=3)
        self.assertViewEqualU(tdict.items(), [('a', 1), ('c', 3), ('b', 2)])

    def test_init_unordered_dict(self):
        tdict = TwoWayOrderedDict({'a': 1, 'b': 2, 'c': 3})
        self.assertViewEqualU(tdict.items(), [('a', 1), ('c', 3), ('b', 2)])


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


class TestSetItem(unittest.TestSuite):

    """Test suite for the TwoWayOrderedDict __setitem__ method.

    Groups together all the test cases for the __setitem__ method
    to organize the code better.

    Test cases are based on the following table:

        .-------.-----------.--------.----------.---------.
        |       | Not Exist | As Key | As Value | As Both |
        :-------+-----------+--------+----------+---------:
        | key   |         1 |      2 |        3 |       4 |
        :-------+-----------+--------+----------+---------:
        | value |         1 |      2 |        3 |       4 |
        '-------'-----------'--------'----------'---------'

        Available permutations for n=4: n*n => 4*4 = 16 (test-cases)

        Test cases details:

            TestValueNotExist: (1, 1), (2, 1), (3, 1), (4, 1)
            TestValueExistAsKey: (1, 2), (2, 2), (3, 2), (4, 2)
            TestValueExistAsValue: (1, 3), (2, 3), (3, 3), (4, 3)
            TestValueExistAsBoth: (1, 4), (2, 4), (3, 4), (4, 4)

    """

    TEST_CASES_COUNT = 16

    class TestValueNotExist(unittest.TestCase, ExtraAssertions):

        def setUp(self):
            self.tdict = TwoWayOrderedDict([('a', 1), ('b', 'b')])
            self.value = 3

            # Hold the expected dict for each test case. Used on tearDown
            self.expected_dict = {}

        def test_set_item_key_not_exist(self):
            self.tdict['c'] = self.value
            self.assertViewEqualO(self.tdict.items(), [('a', 1), ('b', 'b'), ('c', 3)])

            self.expected_dict = {'a': 1, 1: 'a', 'b': 'b', 'c': 3, 3: 'c'}

        def test_set_item_key_exist_as_key(self):
            self.tdict['a'] = self.value
            self.assertViewEqualO(self.tdict.items(), [('a', 3), ('b', 'b')])

            self.expected_dict = {'a': 3, 3: 'a', 'b': 'b'}

        def test_set_item_key_exist_as_value(self):
            self.tdict[1] = self.value
            self.assertViewEqualO(self.tdict.items(), [('b', 'b'), (1, 3)])

            self.expected_dict = {'b': 'b', 1: 3, 3: 1}

        def test_set_item_key_exist_as_both(self):
            self.tdict['b'] = self.value
            self.assertViewEqualO(self.tdict.items(), [('a', 1), ('b', 3)])

            self.expected_dict = {'a': 1, 1: 'a', 'b': 3, 3: 'b'}


    class TestValueExistAsKey(unittest.TestCase, ExtraAssertions):

        def setUp(self):
            self.tdict = TwoWayOrderedDict([('a', 1), ('b', 'b'), ('c', 3)])
            self.value = 'a'

            # Hold the expected dict for each test case. Used on tearDown
            self.expected_dict = {}

        def test_set_item_key_not_exist(self):
            self.tdict['d'] = self.value
            self.assertViewEqualO(self.tdict.items(), [('b', 'b'), ('c', 3), ('d', 'a')])

            self.expected_dict = {'b': 'b', 'c': 3, 3: 'c', 'd': 'a', 'a': 'd'}

        def test_set_item_key_exist_as_key(self):
            self.tdict['a'] = self.value
            self.assertViewEqualO(self.tdict.items(), [('a', 'a'), ('b', 'b'), ('c', 3)])

            self.expected_dict = {'a': 'a', 'b': 'b', 'c': 3, 3: 'c'}

        def test_set_item_key_exist_as_value(self):
            self.tdict[1] = self.value
            self.assertViewEqualO(self.tdict.items(), [('b', 'b'), ('c', 3), (1, 'a')])

            self.expected_dict = {'b': 'b', 'c': 3, 3: 'c', 1: 'a', 'a': 1}

        def test_set_item_key_exist_as_both(self):
            self.tdict['b'] = self.value
            self.assertViewEqualO(self.tdict.items(), [('b', 'a'), ('c', 3)])

            self.expected_dict = {'b': 'a', 'a': 'b', 'c': 3, 3: 'c'}


    class TestValueExistAsValue(unittest.TestCase, ExtraAssertions):

        def setUp(self):
            self.tdict = TwoWayOrderedDict([('a', 1), ('b', 'b'), ('c', 3)])
            self.value = 1

            # Hold the expected dict for each test case. Used on tearDown
            self.expected_dict = {}

        def test_set_item_key_not_exist(self):
            self.tdict['d'] = self.value
            self.assertViewEqualO(self.tdict.items(), [('b', 'b'), ('c', 3), ('d', 1)])

            self.expected_dict = {'b': 'b', 'c': 3, 3: 'c', 'd': 1, 1: 'd'}

        def test_set_item_key_exist_as_key(self):
            self.tdict['c'] = self.value
            self.assertViewEqualO(self.tdict.items(), [('b', 'b'), ('c', 1)])

            self.expected_dict = {'b': 'b', 'c': 1, 1: 'c'}

        def test_set_item_key_exist_as_value(self):
            self.tdict[1] = self.value
            self.assertViewEqualO(self.tdict.items(), [('b', 'b'), ('c', 3), (1, 1)])

            self.expected_dict = {'b': 'b', 'c': 3, 3: 'c', 1: 1}

        def test_set_item_key_exist_as_both(self):
            self.tdict['b'] = self.value
            self.assertViewEqualO(self.tdict.items(), [('b', 1), ('c', 3)])

            self.expected_dict = {'b': 1, 1: 'b', 'c': 3, 3: 'c'}


    class TestValueExistAsBoth(unittest.TestCase, ExtraAssertions):

        def setUp(self):
            self.tdict = TwoWayOrderedDict([('a', 1), ('b', 'b'), ('c', 3)])
            self.value = 'b'

            # Hold the expected dict for each test case. Used on tearDown
            self.expected_dict = {}

        def test_set_item_key_not_exist(self):
            self.tdict['d'] = self.value
            self.assertViewEqualO(self.tdict.items(), [('a', 1), ('c', 3), ('d', 'b')])

            self.expected_dict = {'a': 1, 1: 'a', 'c': 3, 3: 'c', 'd': 'b', 'b': 'd'}

        def test_set_item_key_exist_as_key(self):
            self.tdict['a'] = self.value
            self.assertViewEqualO(self.tdict.items(), [('a', 'b'), ('c', 3)])

            self.expected_dict = {'a': 'b', 'b': 'a', 'c': 3, 3: 'c'}

        def test_set_item_key_exist_as_value(self):
            self.tdict[1] = self.value
            self.assertViewEqualO(self.tdict.items(), [('c', 3), (1, 'b')])

            self.expected_dict = {'c': 3, 3: 'c', 1: 'b', 'b': 1}

        def test_set_item_key_exist_as_both(self):
            self.tdict['b'] = self.value
            self.assertViewEqualO(self.tdict.items(), [('a', 1), ('b', 'b'), ('c', 3)])

            self.expected_dict = {'a': 1, 1: 'a', 'b': 'b', 'c': 3, 3: 'c'}


    def __init__(self):
        super(TestSetItem, self).__init__()
        test_loader = unittest.TestLoader()

        test_cases = [
            self.TestValueNotExist,
            self.TestValueExistAsKey,
            self.TestValueExistAsValue,
            self.TestValueExistAsBoth
        ]

        for test_case in test_cases:
            # Overwrite the tearDown method for each test case
            test_case.tearDown = self.tearDownForTestCases

            self.addTests(test_loader.loadTestsFromTestCase(test_case))

        assert self.countTestCases() == self.TEST_CASES_COUNT

    @staticmethod
    def tearDownForTestCases(test_case):
        """Test the status of the parent dictionary."""
        current_dict = super(test_case.tdict.__class__, test_case.tdict).copy()
        expected_dict = test_case.expected_dict

        test_case.assertEqual(current_dict, expected_dict)


class TestDelItem(unittest.TestCase, ExtraAssertions):

    """Test case for the TwoWayOrderedDict __delitem__ method."""

    def setUp(self):
        self.tdict = TwoWayOrderedDict([('a', 1), ('b', 'b'), ('c', 3)])

    def test_del_item_by_key(self):
        del self.tdict['a']
        self.assertViewEqualO(self.tdict.items(), [('b', 'b'), ('c', 3)])

    def test_del_item_by_value(self):
        del self.tdict[3]
        self.assertViewEqualO(self.tdict.items(), [('a', 1), ('b', 'b')])

    def test_del_item_not_exist(self):
        self.assertRaises(KeyError, self.tdict.__delitem__, 'd')

    def test_del_item_key_equals_value(self):
        del self.tdict['b']
        self.assertViewEqualO(self.tdict.items(), [('a', 1), ('c', 3)])


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


class TestGetValuesAndKeys(unittest.TestCase, ExtraAssertions):

    """Test case for the TwoWayOrderedDict values() & keys() methods."""

    def setUp(self):
        self.tdict = TwoWayOrderedDict([('a', 1), ('b', 2), ('c', 3)])
        self.tdict_empty = TwoWayOrderedDict()

    def test_get_keys_empty(self):
        self.assertViewEqualO(self.tdict_empty.keys(), [])

    def test_get_keys_not_empty(self):
        self.assertViewEqualO(self.tdict.keys(), ['a', 'b', 'c'])

    def test_get_values_empty(self):
        self.assertViewEqualO(self.tdict_empty.values(), [])

    def test_get_values_not_empty(self):
        self.assertViewEqualO(self.tdict.values(), [1, 2, 3])


class TestPopMethods(unittest.TestCase, ExtraAssertions):

    """Test case for the TwoWayOrderedDict pop() & popitem() methods."""

    def setUp(self):
        self.tdict = TwoWayOrderedDict([('a', 1), ('b', 2), ('c', 3)])

    def test_pop_by_key(self):
        self.assertEqual(self.tdict.pop('a'), 1)
        self.assertViewEqualO(self.tdict.items(), [('b', 2), ('c', 3)])

    def test_pop_by_value(self):
        self.assertEqual(self.tdict.pop(1), 'a')
        self.assertViewEqualO(self.tdict.items(), [('b', 2), ('c', 3)])

    def test_pop_raises(self):
        self.assertRaises(KeyError, self.tdict.pop, 'd')

    def test_pop_with_default_value(self):
        self.assertIsNone(self.tdict.pop('d', None))

    def test_popitem_last(self):
        self.assertEqual(self.tdict.popitem(), ('c', 3))
        self.assertViewEqualO(self.tdict.items(), [('a', 1), ('b', 2)])

    def test_popitem_first(self):
        self.assertEqual(self.tdict.popitem(last=False), ('a', 1))
        self.assertViewEqualO(self.tdict.items(), [('b', 2), ('c', 3)])

    def test_popitem_raises(self):
        while self.tdict: self.tdict.popitem()

        self.assertRaises(KeyError, self.tdict.popitem)


class TestUpdate(unittest.TestCase, ExtraAssertions):

    """Test case for the TwoWayOrderedDict update method."""

    def setUp(self):
        self.tdict = TwoWayOrderedDict([('a', 1), ('b', 2)])

    def test_update_ordered(self):
        self.tdict.update([('a', 10), ('c', 3), ('d', 4), ('e', 5)])
        self.assertViewEqualO(self.tdict.items(), [('a', 10), ('b', 2), ('c', 3), ('d', 4), ('e', 5)])

    def test_update_unordered(self):
        self.tdict.update({'a': 10, 'c': 3, 'd': 4, 'e': 5})
        self.assertViewEqualU(self.tdict.items(), [('a', 10), ('b', 2), ('c', 3), ('e', 5), ('d', 4)])

    def test_update_raises(self):
        self.assertRaises(TypeError, self.tdict.update, [('a', 10)], [('b', 20)])

    def test_update_from_other(self):
        other = TwoWayOrderedDict([('a', 10), ('b', 20), ('c', 30)])
        self.tdict.update(other)
        self.assertViewEqualO(self.tdict.items(), [('a', 10), ('b', 20), ('c', 30)])


class TestSetDefault(unittest.TestCase, ExtraAssertions):

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

        self.assertViewEqualO(self.tdict.items(), [('a', 1), ('b', 2), ('c', None), ('d', 'd')])


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


@unittest.skipIf(sys.version_info >= (3, 0) or sys.version_info < (2, 2),
                 "Current Python version does not support this methods")
class TestOldMethods(unittest.TestCase):

    """Contains test cases for the deprecated methods.

    Deprecated methods:
        iteritems(): Replaced by items().

        iterkeys(): Replaced by keys().

        itervalues(): Replaced by values().

        viewitems(): Replaced by items().

        viewkeys(): Replaced by keys().

        viewvalues(): Replaced by values().

    Note:
        In Python 3.* those methods are not available.

    """

    def setUp(self):
        self.tdict = TwoWayOrderedDict()

    def test_iteritems_raises(self):
        self.assertRaises(NotImplementedError, self.tdict.iteritems)

    def test_iterkeys_raises(self):
        self.assertRaises(NotImplementedError, self.tdict.iterkeys)

    def test_itervalues_raises(self):
        self.assertRaises(NotImplementedError, self.tdict.itervalues)

    def test_viewitems_raises(self):
        self.assertRaises(NotImplementedError, self.tdict.viewitems)

    def test_viewkeys_raises(self):
        self.assertRaises(NotImplementedError, self.tdict.viewkeys)

    def test_viewvalues_raises(self):
        self.assertRaises(NotImplementedError, self.tdict.viewvalues)


########## DictViews section ##########


class TestDictKeysView(unittest.TestCase):

    """Contains all the test cases for the DictKeysView object."""

    def setUp(self):
        self.tdict = TwoWayOrderedDict([('a', 1), ('b', 2)])

        self.keys_view = DictKeysView(self.tdict)
        self.keys = ['a', 'b']

    def test_length(self):
        self.assertEqual(len(self.keys_view), len(self.keys))

    def test_iter(self):
        for index, key in enumerate(self.keys_view):
            self.assertEqual(key, self.keys[index])

    def test_contains(self):
        self.assertIn('a', self.keys_view)
        self.assertNotIn(1, self.keys_view)

    def test_repr(self):
        self.assertEqual(repr(self.keys_view), "dict_keys(['a', 'b'])")


class TestDictValuesView(unittest.TestCase):

    """Contains all the test cases for the DictValuesView object."""

    def setUp(self):
        self.tdict = TwoWayOrderedDict([('a', 1), ('b', 2)])

        self.values_view = DictValuesView(self.tdict)
        self.values = [1, 2]

    def test_length(self):
        self.assertEqual(len(self.values_view), len(self.values))

    def test_iter(self):
        for index, value in enumerate(self.values_view):
            self.assertEqual(value, self.values[index])

    def test_contains(self):
        self.assertIn(1, self.values_view)
        self.assertNotIn('a', self.values_view)

    def test_repr(self):
        self.assertEqual(repr(self.values_view), "dict_values([1, 2])")


class TestDictItemsView(unittest.TestCase):

    """Contains all the test cases for the DictItemsView object."""

    def setUp(self):
        self.tdict = TwoWayOrderedDict([('a', 1), ('b', 2)])

        self.items_view = DictItemsView(self.tdict)
        self.items = [('a', 1), ('b', 2)]

    def test_length(self):
        self.assertEqual(len(self.items_view), len(self.items))

    def test_iter(self):
        for index, item in enumerate(self.items_view):
            self.assertEqual(item, self.items[index])

    def test_contains(self):
        self.assertIn(('a', 1), self.items_view)
        self.assertNotIn('a', self.items_view)
        self.assertNotIn(1, self.items_view)
        self.assertNotIn(('a', 10), self.items_view)

    def test_repr(self):
        self.assertEqual(repr(self.items_view), "dict_items([('a', 1), ('b', 2)])")


def all_tests_suite():
    """Return a test suite with all TestCases - TestSuites in this module."""
    test_cases_list = [
        TestInit,
        TestGetItem,
        TestDelItem,
        TestLength,
        TestIteration,
        TestComparison,
        TestGetValuesAndKeys,
        TestPopMethods,
        TestUpdate,
        TestSetDefault,
        TestCopy,
        TestClear,
        TestOldMethods,
        TestDictKeysView,
        TestDictValuesView,
        TestDictItemsView
    ]

    test_suites_list = [
        TestSetItem
    ]


    suite = unittest.TestSuite()
    loader = unittest.TestLoader()

    for test_case in test_cases_list:
        tests = loader.loadTestsFromTestCase(test_case)
        suite.addTest(tests)

    for test_suite in test_suites_list:
        suite.addTest(test_suite())

    return suite


def main():
    verb_lvl = 2 if "-v" in sys.argv else 1
    failfast_sts = True if "-f" in sys.argv else False

    runner = unittest.TextTestRunner(verbosity=verb_lvl, failfast=failfast_sts)
    runner.run(all_tests_suite())

    #unittest.main()


if __name__ == "__main__":
    main()
