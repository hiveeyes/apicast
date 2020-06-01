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
Display list of states and sites::

    apicast beeflight stations

Display list of site slugs::

    apicast beeflight stations --site-slugs

Acquire information for given site slug ``berlin_brandenburg/potsdam``::

    apicast beeflight forecast --station=berlin_brandenburg/potsdam
