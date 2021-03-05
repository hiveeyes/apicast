# -*- coding: utf-8 -*-
import os
from io import open
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, "README.rst"), encoding="UTF-8").read()

setup(
    name="apicast",
    version="0.8.0",
    description="Python client and HTTP service to access bee flight forecast "
                "information published by Deutscher Wetterdienst (DWD), the "
                "federal meteorological service in Germany.",
    long_description=README,
    license="AGPL 3, EUPL 1.2",
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
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
    keywords="honey bee apis mellifera flight forecast information "
    "dwd cdc deutscher wetterdienst climate data center weather "
    "opendata data acquisition transformation export "
    "geospatial temporal timeseries "
    "sensor network observation "
    "http rest api "
    "json markdown",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "requests>=2,<3",
        "ttl-cache>=1.6,<2",
        "beautifulsoup4>=4,<5",
        "html-table-extractor>=1,<2",
        "python-slugify>=4,<5",
        "docopt>=0.6,<1",
        "jsonpickle>=2,<3"
        "python-slugify>=4,<5",
        "tabulate>=0.8,<1",
        "dateparser>=0.7.4,<1",
        "tzlocal>=2,<3",
    ],
    extras_require={
        "service": [
            "fastapi>=0.55.1,<0.64",
            "uvicorn<=0.13.3",
        ],
    },
    entry_points={"console_scripts": ["apicast = apicast.cli:run"]},
)
