# twodict (Two Way Ordered Dict)
Simple two way ordered dictionary for Python.

See [wiki](https://github.com/MrS0m30n3/twodict/wiki) for more informations.

# INSTALLATION

### Install From Source
1. Download & extract source from [here](https://github.com/MrS0m30n3/twodict/archive/1.0.zip)
2. Change directory into **twodict-1.0/**
3. Run `sudo python setup.py install`

### Install From [Pypi](https://pypi.python.org/pypi/twodict)
1. Run `sudo pip install twodict`

# USAGE
```python
from twodict import TwoWayOrderedDict

d = TwoWayOrderedDict(a=1, b=2)
d['c'] = 3

print d[1]  # Outputs 'a'

print d['a']  # Outputs 1

print d  # Outputs TwoWayOrderedDict([('a', 1), ('b', 2), ('c', 3)])

print d.values()  # Outputs [1, 2, 3]

d['a'] = 2  # TwoWayOrderedDict([('a', 2), ('c', 3)])
```

# AUTHOR
[Sotiris Papadopoulos](https://twitter.com/MrS0m30n3)

# LICENSE
Unlicense (public domain)
