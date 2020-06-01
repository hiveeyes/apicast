# -*- coding: utf-8 -*-
# (c) 2020 Andreas Motl <andreas@hiveeyes.org>
# License: GNU Affero General Public License, Version 3
import json
import logging
from docopt import docopt, DocoptExit
from tabulate import tabulate

from apicast import __appname__, __version__
from apicast.core import grok_beeflight_forecast
from apicast.util import normalize_options, setup_logging

log = logging.getLogger(__name__)


def run():
    """
    Access bee flight forecast information published by Deutscher Wetterdienst (DWD).

    Usage:
      apicast stations
      apicast --url=<url>
      apicast --station=<station>
      apicast --version
      apicast (-h | --help)

    Options:
      --url=<url>                       URL to detail page
      --station=<station>               Station identifier
      --version                         Show version information
      --debug                           Enable debug messages
      -h --help                         Show this screen

    Examples::

        # Display list of stations
        apicast stations

        # Display bee flight forecast for Potsdam
        apicast berlin_brandenburg/potsdam

    """

    name = f'{__appname__} {__version__}'

    # Parse command line arguments
    options = normalize_options(docopt(run.__doc__, version=name))

    # Setup logging
    debug = options.get('debug')
    log_level = logging.INFO
    if debug:
        log_level = logging.DEBUG
    setup_logging(log_level)

    # Debugging
    log.debug('Options: {}'.format(json.dumps(options, indent=4)))

    # Run command.
    if options.url:

        # Fetch and extract forecast information
        result = grok_beeflight_forecast(options.url)

        data = result['data']
        if not data:
            raise ValueError('No data found or unable to parse')

        # Report about weather station / observation location
        print()
        print(u'### Prognose des Bienenfluges in {}'.format(result['station']))
        print()

        # Output forecast data
        print(tabulate(data[1:], headers=data[0], showindex=False, tablefmt='pipe'))
