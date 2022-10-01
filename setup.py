# -*- coding: utf-8 -*-

"""Setup for dwdwfsapi package."""

from setuptools import setup, find_packages

# Package meta-data
NAME = "dwdwfsapi"
DESCRIPTION = (
    "Python client to retrieve data provided by DWD via their geoserver "
    "WFS API"
)
KEYWORDS = "dwd ows wfs deutscher wetterdienst"
URL = "https://github.com/stephan192/dwdwfsapi"
EMAIL = "stephan192@outlook.com"
AUTHOR = "stephan192"
REQUIRES_PYTHON = ">=3.6"
VERSION = "1.0.6"

# Define required packages
REQUIRES = ["requests>=2.23.0,<3", "ciso8601>=2.1.3,<3", "urllib3>=1.25.8,<2"]

# Import README.md and CHANGELOG.md
with open("README.md", "r") as fh:
    LONG_DESCRIPTION = fh.read()

# Calling setup
setup(
    name=NAME,
    version=VERSION,
    author=AUTHOR,
    author_email=EMAIL,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    url=URL,
    packages=find_packages(),
    install_requires=REQUIRES,
    keywords=KEYWORDS,
    license="MIT",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=REQUIRES_PYTHON,
)
