#######
Apicast
#######


*****
About
*****

Apicast acquires bee flight forecast information published by Deutscher Wetterdienst (DWD).

- **Source**:

  - https://www.dwd.de/DE/leistungen/biene_flug/bienenflug.html
  - https://www.dwd.de/DE/fachnutzer/freizeitgaertner/1_gartenwetter/_node.html

- **Documentation**:

  - https://www.dwd.de/DE/fachnutzer/freizeitgaertner/dokumentation/gw_bienenflug
  - https://www.dwd.de/DE/fachnutzer/freizeitgaertner/dokumentation/gw_bienenflug.pdf?__blob=publicationFile
  - https://community.hiveeyes.org/t/dwd-prognose-bienenflug/787

- **Data copyright**: © Deutscher Wetterdienst (DWD), Abteilung Agrarmeteorologie

- **Live**: http://apicast.hiveeyes.org/


*****
Setup
*****

CLI version::

    pip install apicast

HTTP API variant::

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

There are different endpoints and query parameters. Go figure:

- http://localhost:24640/beeflight/stations/germany
- http://localhost:24640/beeflight/stations/germany/locations
- http://localhost:24640/beeflight/forecast/germany/brandenburg/potsdam?translate=false
- http://localhost:24640/beeflight/forecast/germany/brandenburg/potsdam?translate=true
- http://localhost:24640/beeflight/forecast/germany/brandenburg/potsdam?format=json
- http://localhost:24640/beeflight/forecast/germany/brandenburg/potsdam?format=table-markdown
- http://localhost:24640/beeflight/forecast/germany/brandenburg/potsdam?format=json-machine


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
