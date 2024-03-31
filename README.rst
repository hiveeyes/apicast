#######
Apicast
#######

|

.. start-badges

|ci-tests| |ci-coverage| |license| |pypi-downloads|
|python-versions| |status| |pypi-version|

.. |ci-tests| image:: https://github.com/hiveeyes/apicast/workflows/Tests/badge.svg
    :target: https://github.com/hiveeyes/apicast/actions?workflow=Tests

.. |ci-coverage| image:: https://codecov.io/gh/hiveeyes/apicast/branch/main/graph/badge.svg
    :target: https://codecov.io/gh/hiveeyes/apicast
    :alt: Test suite code coverage

.. |python-versions| image:: https://img.shields.io/pypi/pyversions/apicast.svg
    :target: https://python.org

.. |pypi-version| image:: https://img.shields.io/pypi/v/apicast.svg
    :target: https://pypi.org/project/apicast/

.. |status| image:: https://img.shields.io/pypi/status/apicast.svg
    :target: https://pypi.org/project/apicast/

.. |license| image:: https://img.shields.io/pypi/l/apicast.svg
    :target: https://pypi.org/project/apicast/

.. |pypi-downloads| image:: https://static.pepy.tech/badge/apicast/month
    :target: https://pepy.tech/project/apicast

.. end-badges


*****
About
*****

Apicast acquires bee flight forecast information published by Deutscher Wetterdienst (DWD).

- **Development**: `Hiveeyes » DWD-Prognose Bienenflug`_
- **Live API**: https://apicast.hiveeyes.org/ (also on HTTP)


*****
Setup
*****

CLI version::

    pip install apicast

HTTP API::

    pip install apicast[service]


********
Synopsis
********

Display list of states and sites::

    apicast beeflight stations

Display list of location slugs::

    apicast beeflight stations --slugs

Acquire information for given location slug ``brandenburg/potsdam``::

    apicast beeflight forecast --station=brandenburg/potsdam

Acquire information for given location slug ``brandenburg/potsdam``, output as table in Markdown format::

    apicast beeflight forecast --station=brandenburg/potsdam --format=table-markdown

Output as table in JSON machine readable format::

    apicast beeflight forecast --station=brandenburg/potsdam --format=json-machine



********
HTTP API
********

Start HTTP API service::

    apicast service

Start HTTP service with dynamic code reloading::

    apicast service --reload

Then navigate to::

    open http://localhost:24640/



*******
Example
*******

::

    apicast beeflight forecast --station=brandenburg/potsdam

::

    [
        {
            "Datum": "Mo 01.06.",
            "morgens": "stark",
            "mittags": "intensiv",
            "abends": "stark"
        },
        {
            "Datum": "Di 02.06.",
            "morgens": "stark",
            "mittags": "intensiv",
            "abends": "intensiv"
        },
        {
            "Datum": "Mi 03.06.",
            "morgens": "intensiv",
            "mittags": "intensiv",
            "abends": "intensiv"
        }
    ]


*****
Tests
*****

::

    make test


********************
Content attributions
********************

The copyright of data, particular images and pictograms are held by their respective owners, unless otherwise noted.

Data
====

- **Source**:

  - https://www.dwd.de/DE/leistungen/biene_flug/bienenflug.html
  - https://www.dwd.de/DE/fachnutzer/freizeitgaertner/1_gartenwetter/_node.html

- **Documentation**:

  - https://www.dwd.de/DE/fachnutzer/landwirtschaft/dokumentationen/allgemein/bienenflug_doku.html
  - https://www.dwd.de/DE/fachnutzer/landwirtschaft/dokumentationen/isabel/meinagrar_bienenflug.html
  - https://www.dwd.de/DE/klimaumwelt/ku_beratung/landwirtschaft/agrar_modelle/Bienenflug.pdf?__blob=publicationFile

- **Data copyright**: © Deutscher Wetterdienst (DWD), Agricultural Meteorology Department


Logo picture
============

- **Description**:     	A bee swarm on an oak tree in Plymouth, UK
- **Date**:    	        21 June 2009
- **Source**: 	        Own work
- **Author**: 	        Nilfanion
- **Camera location**:	50° 24′ 38.3″ N, 4° 09′ 28.2″ W
- **License**:          Creative Commons Attribution-Share Alike 3.0 Unported
- **URL**:              https://commons.wikimedia.org/wiki/File:Bee_swarm_in_Plymouth.jpg


.. _Hiveeyes » DWD-Prognose Bienenflug: https://community.hiveeyes.org/t/dwd-prognose-bienenflug/787
