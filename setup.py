import multiprocessing
from setuptools import setup, find_packages
import os
import glob

with open("README.md", "r") as fh:
    long_description = fh.read()


setup(
    name = "logging_singleton",
    version = "0.0.1",

    packages = find_packages(where="src"),
    package_dir = {"": "src"},

    # Dependencies on other packages:
    #setup_requires   = ['pytest-runner'],
    install_requires = [
                        ],

    # Unit tests; they are initiated via 'python setup.py test'
    #test_suite       = 'nose.collector',
    #test_suite       = 'tests',
    #test_suite        = 'unittest2.collector',
    #tests_require    =['pytest',
    #                   'testfixtures>=6.14.1',
    #                   ],

    # metadata for upload to PyPI
    author = "Andreas Paepcke",
    author_email = "paepcke@cs.stanford.edu",
    description = "Simple logging service shared by all application modules",
    long_description_content_type = "text/markdown",
    long_description = long_description,
    license = "BSD",
    url = "git@github.com:paepcke/logging_singleton.git",   # project home page, if any
)
