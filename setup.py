# -*- coding: utf-8 -*-
"""
Dictionaries that survive one run
"""
import setuptools

# We use semantic versioning http://semver.org/.
#
# Summary: Given a version number MAJOR.MINOR.PATCH, we increment the:
#
#     MAJOR for incompatible API changes,
#     MINOR for added functionality in a backwards-compatible manner
#     PATCH for backwards-compatible bug fixes.
#
# Additionally, for dev, release candidates, and post releases, we respect
# https://www.python.org/dev/peps/pep-0440/ by suffixing accordingly.

version = open("version").read()

package_name = "persistentdicts"
description = __doc__
github_url = version

if "dev" in version:
    package_name = "persistentdicts-dev"
    description = "development version of persistentdicts"
    github_url = "master"

setuptools.setup(
    name=package_name,
    version=version,
    description=description,
    author="Christophe-Marie Duquesne",
    author_email ="chmd@chmd.fr",
    url="https://github.com/chmduquesne/persistentdicts",
    download_url="https://github.com/chmduquesne/persistentdicts/archive/%s.tar.gz" % (github_url),
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
        "kyotocabinet >= 1.9"
        ]
)
