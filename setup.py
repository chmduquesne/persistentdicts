# -*- coding: utf-8 -*-
"""
dict-like interfaces for various databases
"""
import setuptools
import re
import sys
from subprocess import check_output as run

NAME = "persistentdicts"
DOWNLOAD_URL = "https://github.com/chmduquesne/%s/archive/%s.tar.gz"

# We use semantic versioning http://semver.org/.
#
# Given a version number MAJOR.MINOR.PATCH, we increment the:
#
#     MAJOR for incompatible API changes,
#     MINOR for added functionality in a backwards-compatible manner
#     PATCH for backwards-compatible bug fixes.
RELEASE = "1.2.2"

# Get the version from git, otherwise fall back to RELEASE
try:
    VERSION = re.sub("-(\\d+)-\\w+$", ".dev\\1", run(["git", "describe"]).strip())
except subprocess.CalledProcessError:
    VERSION = RELEASE

# Make sure we are not releasing something poorly tagged
if not VERSION.startswith(RELEASE):
    sys.exit("The git tag does not match the release. Please fix.")

if "dev" not in VERSION:
    # release
    PACKAGE_NAME = NAME
    DESCRIPTION = __doc__
    GIT_REF = RELEASE
else:
    # dev version
    PACKAGE_NAME = NAME + "-dev"
    DESCRIPTION = "development version of %s" % NAME
    GIT_REF = "master"

setuptools.setup(
    name=PACKAGE_NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=open("README.rst").read(),
    author="Christophe-Marie Duquesne",
    author_email="chmd@chmd.fr",
    url="https://github.com/chmduquesne/%s" % NAME,
    download_url=DOWNLOAD_URL % (NAME, GIT_REF),
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
