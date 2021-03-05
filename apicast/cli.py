# -*- coding: utf-8 -*-
# (c) 2018-2021 Andreas Motl <andreas@hiveeyes.org>
# License: GNU Affero General Public License, Version 3
import json
import logging

import jsonpickle
from docopt import docopt

from apicast import __appname__, __version__
from apicast.core import DwdBeeflightForecast
from apicast.format import Formatter
from apicast.util import normalize_options, setup_logging

log = logging.getLogger(__name__)


def run():
    """
    Access bee flight forecast information published by Deutscher Wetterdienst (DWD).

    Usage:
      apicast beeflight stations [--slugs]
      apicast beeflight forecast --station=<station> [--format=<format>]
      apicast service [--listen=<listen>] [--reload]
      apicast --version
      apicast (-h | --help)

    Options:
      --url=<url>                       URL to detail page
      --station=<station>               Station identifier
      --format=<format>                 Output format: "json", "json-machine" or "table-markdown". Default: json
      --listen=<listen>                 HTTP server listen address. [Default: localhost:24640]
      --version                         Show version information
      --debug                           Enable debug messages
      -h --help                         Show this screen

    Examples::

        # Display list of stations
        apicast beeflight stations

        # Display list of station slugs
        apicast beeflight stations --slugs

        # Display bee flight forecast for Potsdam in JSON format
        apicast beeflight forecast --station=brandenburg/potsdam

        # Display bee flight forecast for Potsdam in Markdown format
        apicast beeflight forecast --station=brandenburg/potsdam --format=table-markdown

        # Display bee flight forecast for Potsdam in JSON machine readable format
        apicast beeflight forecast --station=brandenburg/potsdam --format=json-machine

        # Start HTTP service
        apicast service

        # Start HTTP service with dynamic code reloading
        apicast service --reload

    """

    name = f"{__appname__} {__version__}"

    # Parse command line arguments
    options = normalize_options(docopt(run.__doc__, version=name))

    # Setup logging
    debug = options.get("debug")
    log_level = logging.INFO
    if debug:
        log_level = logging.DEBUG
    setup_logging(log_level)

    # Debugging
    log.debug("Options: {}".format(json.dumps(options, indent=4)))

    # Run service.
    if options.service:
        listen_address = options.listen
        log.info(f"Starting {name}")
        log.info(f"Starting web service on {listen_address}")
        from apicast.api import start_service

        start_service(listen_address, options.reload)
        return

    dbf = DwdBeeflightForecast()

    # Run command.
    if options.stations:

        if options.slugs:
            result = dbf.get_station_slugs()
            print("\n".join(result))

        else:
            result = dbf.get_stations()
            print(jsonpickle.encode(result, unpicklable=False, indent=4))

    # Fetch and extract forecast information.
    elif options.station:
        station = dbf.get_station_by_slug(options.station)
        result = dbf.get_data(station=station)
        format_beeflight_forecast(result, options.format)


def format_beeflight_forecast(result, format="json"):

    if not result.data:
        raise ValueError("No data found or unable to parse")

    format = format or "json"
    format = format.lower()

    if format == "json":
        response = Formatter(result).normalize()
        print(json.dumps(response, indent=4))

    elif format == "json-machine":
        response = Formatter(result).machinify()
        print(json.dumps(response, indent=4))

    elif format == "table-markdown":
        response = Formatter(result).table_markdown()
        print(response)

    else:
        raise ValueError(
            'Unknown output format. Please specify "json", "json-machine" or "table-markdown".'
        )
