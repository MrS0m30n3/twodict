
"""Two Way Ordered DICTionary for Python.

Attributes:
    _RANDOM_OBJECT (object): Object that it's used as a default parameter.

"""

_RANDOM_OBJECT = object()


class TwoWayOrderedDict(dict):

    """Custom data structure which implements a two way ordrered dictionary.

    TwoWayOrderedDict it's a custom dictionary in which you can get the
    key:value relationship but you can also get the value:key relationship.
    It also remembers the order in which the items were inserted and supports
    almost all the features of the build-in dict.

    Note:
        Ways to create a new dictionary.

        *) d = TwoWayOrderedDict(a=1, b=2) (Unordered)
        *) d = TwoWayOrderedDict({'a': 1, 'b': 2}) (Unordered)

        *) d = TwoWayOrderedDict([('a', 1), ('b', 2)]) (Ordered)
        *) d = TwoWayOrderedDict(zip(['a', 'b', 'c'], [1, 2, 3])) (Ordered)

    Examples:
        >>> d = TwoWayOrderedDict(a=1, b=2)
        >>> d['a']
        1
        >>> d[1]
        'a'
        >>> print d
        TwoWayOrderedDict([('a', 1), ('b', 2)])

    """

    _PREV = 0
    _KEY = 1
    _NEXT = 2

    def __init__(self, *args, **kwargs):
        self._items = item = []
        self._items += [item, None, item]  # Double linked list [prev, key, next]
        self._items_map = {}  # Map link list items into keys to speed up lookup
        self._load(args, kwargs)

    def __setitem__(self, key, value):
        if key in self:
            # If self[key] == key for example {'b': 'b'} and we
            # do d['b'] = 2 then we dont want to remove the 'b'
            # from our linked list because we will lose the order
            if self[key] in self._items_map and key != self[key]:
                self._remove_mapped_key(self[key])

            dict.__delitem__(self, self[key])

        if value in self:
            # If value == key we dont have to remove the
            # value from the items_map because the value is
            # the key and we want to keep the key in our
            # linked list in order to keep the order.
            if value in self._items_map and key != value:
                self._remove_mapped_key(value)

            if self[value] in self._items_map:
                self._remove_mapped_key(self[value])

            # Check if self[value] is in the dict
            # for cases like {'a': 'a'} where we
            # have only one copy instead of {'a': 1, 1: 'a'}
            if self[value] in self:
                dict.__delitem__(self, self[value])

        if key not in self._items_map:
            last = self._items[self._PREV]  # self._items prev always points to the last item
            last[self._NEXT] = self._items[self._PREV] = self._items_map[key] = [last, key, self._items]

        dict.__setitem__(self, key, value)
        dict.__setitem__(self, value, key)

    def __delitem__(self, key):
        if self[key] in self._items_map:
            self._remove_mapped_key(self[key])

        if key in self._items_map:
            self._remove_mapped_key(key)

        dict.__delitem__(self, self[key])

        # Check if key is in the dict
        # for cases like {'a': 'a'} where we
        # have only one copy instead of {'a': 1, 1: 'a'}
        if key in self:
            dict.__delitem__(self, key)

    def __len__(self):
        return len(self._items_map)

    def __iter__(self):
        curr = self._items[self._NEXT]
        while curr is not self._items:
            yield curr[self._KEY]
            curr = curr[self._NEXT]

    def __reversed__(self):
        curr = self._items[self._PREV]
        while curr is not self._items:
            yield curr[self._KEY]
            curr = curr[self._PREV]

    def __repr__(self):
        return '%s(%r)' % (self.__class__.__name__, self.items())

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.items() == other.items()
        return False

    def __ne__(self, other):
        return not self == other

    def _remove_mapped_key(self, key):
        """Remove the given key both from the linked list
        and the map dictionary. """
        prev, __, next = self._items_map.pop(key)
        prev[self._NEXT] = next
        next[self._PREV] = prev

    def _load(self, args, kwargs):
        """Load items into our dictionary. """
        for item in args:
            if type(item) == dict:
                item = item.iteritems()

            for key, value in item:
                self[key] = value

        for key, value in kwargs.items():
            self[key] = value

    def items(self):
        return [(key, self[key]) for key in self]

    def values(self):
        return [self[key] for key in self]

    def keys(self):
        return list(self)

    def pop(self, key, default=_RANDOM_OBJECT):
        try:
            value = self[key]

            del self[key]
        except KeyError as error:
            if default == _RANDOM_OBJECT:
                raise error

            value = default

        return value

    def popitem(self, last=True):
        """Remove and return a (key, value) pair from the dictionary.
        If the dictionary is empty calling popitem() raises a KeyError.

        Args:
            last (bool): When False popitem() will remove the first item
                from the list.

        Note:
            popitem() is useful to destructively iterate over a dictionary.

        Raises:
            KeyError

        """
        if not self:
            raise KeyError('popitem(): dictionary is empty')

        if last:
            __, key, __ = self._items[self._PREV]
        else:
            __, key, __ = self._items[self._NEXT]

        value = self.pop(key)

        return key, value

    def update(self, *args, **kwargs):
        self._load(args, kwargs)

    def setdefault(self, key, default=None):
        try:
            return self[key]
        except KeyError:
            self[key] = default
            return default

    def copy(self):
        return self.__class__(self.items())

    def clear(self):
        self._items = item = []
        self._items += [item, None, item]
        self._items_map = {}
        dict.clear(self)
