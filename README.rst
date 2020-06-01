#######
Apicast
#######


*****
About
*****
Apicast acquires bee flight forecast information published by Deutscher Wetterdienst (DWD).


********
Synopsis
********
Acquire list of stations::

    ./extract_sites.sh

Acquire information for given location ``berlin_brandenburg/potsdam``::

    apicast --url https://www.dwd.de/DE/fachnutzer/freizeitgaertner/1_gartenwetter/berlin_brandenburg/potsdam/_node.html
