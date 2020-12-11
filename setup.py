from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()


setup(
    name = "logging-singleton",
    version = "0.13",

    package_dir = {'': 'src'},
    packages = ['logging_service'],
    download_url = 'https://github.com/paepcke/logging_singleton/archive/v0.0.3.tar.gz',

    # metadata for upload to PyPI
    author = "Andreas Paepcke",
    author_email = "paepcke@cs.stanford.edu",
    description = "Simple logging service shared by all application modules",
    long_description_content_type = "text/markdown",
    long_description = long_description,
    license = "BSD",
    url = "https://github.com/paepcke/logging_singleton.git",   # project home page, if any
)
