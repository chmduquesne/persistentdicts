# -*- coding: utf-8 -*-
"""
Dictionaries that survive one run
"""
import setuptools

version="0.0.1"

setuptools.setup(
    name="persistentdicts",
    version=version,
    description=__doc__,
    author="Christophe-Marie Duquesne",
    author_email ="chmd@chmd.fr",
    url="https://github.com/chmduquesne/persistentdicts",
    download_url="https://github.com/chmduquesne/persistentdicts/tarball/%s" % (version),
    keywords=["database", "interface", "adapter"]
    packages=["persistentdicts"],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        ]
    install_requires=[
        "kyotocabinet >= 1.9"
        ]
)
