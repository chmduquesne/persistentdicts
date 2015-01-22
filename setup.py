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
if version.contains("dev"):
    github_download = "master"
else:
    github_download = version

setuptools.setup(
    name="persistentdicts",
    version=version,
    description=__doc__,
    author="Christophe-Marie Duquesne",
    author_email ="chmd@chmd.fr",
    url="https://github.com/chmduquesne/persistentdicts",
    download_url="https://github.com/chmduquesne/persistentdicts/archive/%s.tar.gz" % (github_download),
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
