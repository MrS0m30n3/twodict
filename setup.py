#!/usr/bin/env python
# -*- coding: utf-8 -*-

from distutils.core import setup

from twodict import __version__, __license__


setup(
    author       = "Sotiris Papadopoulos",
    author_email = "ytubedlg@gmail.com",
    name         = "twodict",
    description  = "Simple two way ordered dictionary for Python",
    version      = __version__,
    license      = __license__,
    url          = "https://github.com/MrS0m30n3/twodict",
    py_modules   = ["twodict"]
)
