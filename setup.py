# -*- coding: utf-8 -*-
import os
from io import open

from setuptools import find_packages, setup

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, "README.rst"), encoding="UTF-8").read()

setup(
    name="apicast",
    version="0.9.0",
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
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
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
        "beautifulsoup4>=4,<5",
        "dateparser>=0.7.4,<2",
        "docopt-ng>=0.6,<0.10",
        "html-table-extractor>=1,<2",
        "jsonpickle>=2,<4",
        "munch>=2.5,<5",
        "python-slugify>=4,<9",
        "requests>=2.25.2,<3",
        "tabulate>=0.8,<0.10",
        "ttl-cache>=1.6,<2",
        "tzlocal>=2,<6",
    ],
    extras_require={
        "service": [
            "fastapi>=0.55.1,<0.111",
            "httpx<1",
            "uvicorn<=0.29.0",
        ],
    },
    entry_points={"console_scripts": ["apicast = apicast.cli:run"]},
)
