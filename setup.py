# -*- coding: utf-8 -*-
"""
Dictionaries that survive one run
"""
import setuptools

setuptools.setup(
    name="persistentdicts",
    version='0.0.1',
    long_description=__doc__,
    packages=["persistentdicts"],
    install_requires=[
        "kyotocabinet >= 1.9"
        ]
)
