# -*- coding: utf-8 -*-
import os
from io import open
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, "README.rst"), encoding="UTF-8").read()

setup(
    name="apicast",
    version="0.2.0",
    description="Python client to access bee flight forecast information published by Deutscher Wetterdienst (DWD), "
    "the federal meteorological service in Germany.",
    long_description=README,
    license="AGPL 3, EUPL 1.2",
    classifiers=[
        "Programming Language :: Python",
        "License :: OSI Approved :: European Union Public Licence 1.2 (EUPL 1.2)",
        "License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)",
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Information Technology",
        "Intended Audience :: Science/Research",
        "Topic :: Communications",
        "Topic :: Database",
        "Topic :: Internet",
        "Topic :: Scientific/Engineering :: Atmospheric Science",
        "Topic :: Scientific/Engineering :: GIS",
        "Topic :: Scientific/Engineering :: Human Machine Interfaces",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Scientific/Engineering :: Interface Engine/Protocol Translator",
        "Topic :: Scientific/Engineering :: Visualization",
        "Topic :: Software Development :: Libraries",
        "Topic :: System :: Archiving",
        "Topic :: Text Processing",
        "Topic :: Utilities",
        "Operating System :: POSIX",
        "Operating System :: Unix",
        "Operating System :: MacOS",
    ],
    author="Andreas Motl",
    author_email="andreas@hiveeyes.org",
    url="https://github.com/hiveeyes/apicast",
    keywords="bee flight forecast information "
    "dwd cdc deutscher wetterdienst climate data center weather "
    "opendata data acquisition transformation export "
    "geospatial temporal timeseries "
    "sensor network observation "
    "http rest api "
    "json csv",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "MechanicalSoup==0.12.0",
        "html-table-extractor==1.4.1",
        "tabulate==0.8.7",
        "docopt==0.6.2",
        "munch==2.5.0",
    ],
    entry_points={"console_scripts": ["apicast = apicast.cli:run"]},
)
