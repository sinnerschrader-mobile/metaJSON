#!/usr/bin/env python
import re
from setuptools import setup

version = re.search(
    '^__version__\s*=\s*"(.*)"',
    open('metajson/readJSON.py').read(),
    re.M
    ).group(1)


with open("README.md", "rb") as f:
    long_descr = f.read().decode("utf-8")

setup(
    name = "metaJSON",
    packages = ["metajson"],
    entry_points = {
        "console_scripts": ['metajson = metajson.readJSON:main']
        },
    install_requires = ['pystache'],
    tests_require = ['nose'],
    include_package_data = True, #will include files listed in MANIFEST.in
    version = version,
    description = 'metaJSON provides a meta language to generate object models for several languages. The generated classes can easily be used for the client-server communication.',
    url = 'https://github.com/sinnerschrader-mobile/metaJSON.git',
    license = 'MIT',
    long_description = long_descr,
    )
