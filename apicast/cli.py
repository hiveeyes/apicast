# -*- coding: utf-8 -*-
# (c) 2018-2020 Andreas Motl <andreas@hiveeyes.org>
# License: GNU Affero General Public License, Version 3
import json
import logging
import tabulate
from docopt import docopt, DocoptExit

from apicast import __appname__, __version__
from apicast.core import grok_beeflight_forecast, dwd_beeflight_forecast_stations, dwd_beeflight_site_url_by_slug
from apicast.util import normalize_options, setup_logging

log = logging.getLogger(__name__)


def run():
    """
    Access bee flight forecast information published by Deutscher Wetterdienst (DWD).

    Usage:
      apicast beeflight stations [--site-slugs]
      apicast beeflight forecast --url=<url> [--format=<format>]
      apicast beeflight forecast --station=<station> [--format=<format>]
      apicast --version
      apicast (-h | --help)

    Options:
      --url=<url>                       URL to detail page
      --station=<station>               Station identifier
      --format=<format>                 Output format: "json" or "table". Default: json
      --version                         Show version information
      --debug                           Enable debug messages
      -h --help                         Show this screen

    Examples::

        # Display list of stations
        apicast stations

        # Display bee flight forecast for Potsdam
        apicast --station=berlin_brandenburg/potsdam

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
    if options.stations:
        stations = dwd_beeflight_forecast_stations()

        if options.site_slugs:
            slugs = []
            for station in stations:
                for site in station.sites:
                    slugs.append(site.slug)
            print(json.dumps(slugs, indent=4))
        else:
            print(json.dumps(stations, indent=4))

    # Fetch and extract forecast information.
    elif options.url:
        result = grok_beeflight_forecast(options.url)
        format_beeflight_forecast(result, options.format)

    elif options.station:
        url = dwd_beeflight_site_url_by_slug(options.station)
        result = grok_beeflight_forecast(url)
        format_beeflight_forecast(result, options.format)


def format_beeflight_forecast(result, format='json'):

    data = result['data']
    if not data:
        raise ValueError('No data found or unable to parse')

    format = format or 'json'
    format = format.lower()

    if format not in ['json', 'table']:
        raise ValueError('Unknown output format. Please specify "json" or "table".')

    if format == 'json':
        result = []
        for item in data[1:]:
            item = dict(zip(data[0], item))
            result.append(item)
        print(json.dumps(result, indent=4))

    else:

        # Report about weather station / observation location
        print()
        print(u'### Prognose des Bienenfluges in {}'.format(result['station']))
        print()

        # Output forecast data
        print(tabulate.tabulate(data[1:], headers=data[0], showindex=False, tablefmt='pipe'))
