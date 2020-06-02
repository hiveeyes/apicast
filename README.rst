#######
Apicast
#######


*****
About
*****
Apicast acquires bee flight forecast information published by Deutscher Wetterdienst (DWD).

https://www.dwd.de/DE/fachnutzer/freizeitgaertner/1_gartenwetter/_node.html


********
Synopsis
********
Display list of states and sites::

    apicast beeflight stations

Display list of site slugs::

    apicast beeflight stations --site-slugs

Acquire information for given site slug ``berlin_brandenburg/potsdam``::

    apicast beeflight forecast --station=berlin_brandenburg/potsdam

Acquire information for given site slug ``berlin_brandenburg/potsdam``, output as table in Markdown format::

    apicast beeflight forecast --station=berlin_brandenburg/potsdam --format=table

Start HTTP API service::

    apicast service


*******
Example
*******

::

    apicast beeflight forecast --station=berlin_brandenburg/potsdam

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
