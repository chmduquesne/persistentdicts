# -*- coding: utf-8 -*-
"""
Dictionaries that survive one run
"""
import setuptools

version="0.0.2"

setuptools.setup(
    name="persistentdicts",
    packages=["persistentdicts"],
    version=version,
    description=__doc__,
    author="Christophe-Marie Duquesne",
    author_email ="chmd@chmd.fr",
    url="https://github.com/chmduquesne/persistentdicts",
    download_url="https://github.com/chmduquesne/persistentdicts/archive/%s.tar.gz" % (version),
    keywords=["database", "interface", "adapter"],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        ],
    install_requires=[
        "kyotocabinet >= 1.9"
        ]
)
