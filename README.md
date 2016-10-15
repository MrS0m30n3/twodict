# twodict (Two Way Ordered Dict)
Simple two way ordered dictionary for Python.

See [wiki](https://github.com/MrS0m30n3/twodict/wiki) for more informations.

# INSTALLATION

### Install From Source
1. Download & extract source from [here](https://github.com/MrS0m30n3/twodict/archive/1.2.zip)
2. Change directory into **twodict-1.2/**
3. Run `sudo python setup.py install`

### Install From [Pypi](https://pypi.python.org/pypi/twodict)
1. Run `sudo pip install twodict`

# USAGE
```python
from twodict import TwoWayOrderedDict

tdict = TwoWayOrderedDict()
tdict['a'] = 1
tdict['b'] = 2
tdict['c'] = 3

print(tdict['a'])  # Outputs 1
print(tdict[1])  # Outputs 'a'

del tdict[2]
print(tdict)  # TwoWayOrderedDict([('a', 1), ('c', 3)])
```

# AUTHOR
[Sotiris Papadopoulos](https://twitter.com/MrS0m30n3)

# LICENSE
Unlicense (public domain)
