# -*- coding: utf-8 -*-
# (c) 2018-2020 Andreas Motl <andreas@hiveeyes.org>
# License: GNU Affero General Public License, Version 3
import json
import logging
import tabulate
from docopt import docopt, DocoptExit

from apicast import __appname__, __version__
from apicast.core import dwd_beeflight_forecast_data, dwd_beeflight_forecast_stations, dwd_beeflight_site_url_by_slug, \
    dwd_beeflight_forecast_stations_site_slugs
from apicast.util import normalize_options, setup_logging

log = logging.getLogger(__name__)


def run():
    """
    Access bee flight forecast information published by Deutscher Wetterdienst (DWD).

    Usage:
      apicast beeflight stations [--site-slugs]
      apicast beeflight forecast --url=<url> [--format=<format>]
      apicast beeflight forecast --station=<station> [--format=<format>]
      apicast service [--listen=<listen>]
      apicast --version
      apicast (-h | --help)

    Options:
      --url=<url>                       URL to detail page
      --station=<station>               Station identifier
      --format=<format>                 Output format: "json" or "table". Default: json
      --listen=<listen>                 HTTP server listen address. [Default: localhost:24640]
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

    # Run service.
    if options.service:
        listen_address = options.listen
        log.info(f'Starting {name}')
        log.info(f'Starting web service on {listen_address}')
        from apicast.api import start_service
        start_service(listen_address)
        return

    # Run command.
    if options.stations:

        if options.site_slugs:
            result = dwd_beeflight_forecast_stations_site_slugs()

        else:
            result = dwd_beeflight_forecast_stations()

        print(json.dumps(result, indent=4))

    # Fetch and extract forecast information.
    elif options.url:
        result = dwd_beeflight_forecast_data(options.url)
        format_beeflight_forecast(result, options.format)

    elif options.station:
        url = dwd_beeflight_site_url_by_slug(options.station)
        result = dwd_beeflight_forecast_data(url)
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
