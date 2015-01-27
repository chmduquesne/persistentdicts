# -*- coding: utf-8 -*-
"""
Databases exposed through dict-like objects (sqlite, kyotocabinet)
"""
import setuptools

DOWNLOAD = "https://github.com/chmduquesne/persistentdicts/archive/%s.tar.gz"

# We use semantic versioning http://semver.org/.
#
# Summary: Given a version number MAJOR.MINOR.PATCH, we increment the:
#
#     MAJOR for incompatible API changes,
#     MINOR for added functionality in a backwards-compatible manner
#     PATCH for backwards-compatible bug fixes.
VERSION = open("version").read().strip()

PACKAGE_NAME = "persistentdicts"
DESCRIPTION = __doc__
GIT_REF = VERSION


# We also have travis-ci generate a version file that contains the most
# recent tag, followed by dev and the number of revisions since that tag
# (in respect with https://www.python.org/dev/peps/pep-0440/), and we
# maintain a bleeding-edge version.
if "dev" in VERSION:
    PACKAGE_NAME = "persistentdicts-dev"
    DESCRIPTION = "development version of persistentdicts"
    GIT_REF = "master"

setuptools.setup(
    name=PACKAGE_NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=open("README.md").read(),
    author="Christophe-Marie Duquesne",
    author_email="chmd@chmd.fr",
    url="https://github.com/chmduquesne/persistentdicts",
    download_url=DOWNLOAD % (GIT_REF),
    keywords=["database", "interface", "adapter"],
    packages=["persistentdicts"],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        ],
    install_requires=[
        "kyotocabinet >= 1.9",
        "cassandra-driver >= 2.1.3"
        ]
)
