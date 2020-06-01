# -*- coding: utf-8 -*-
# (c) 2019 Andreas Motl <andreas@terkin.org>
# License: GNU Affero General Public License, Version 3
import sys
import logging
from munch import munchify

log = logging.getLogger(__name__)


def setup_logging(level=logging.INFO):
    log_format = '%(asctime)-15s [%(name)-22s] %(levelname)-7s: %(message)s'
    logging.basicConfig(
        format=log_format,
        stream=sys.stderr,
        level=level)


def configure_http_logging(options):
    # Control debug logging of HTTP requests.

    if options.http_logging:
        log_level = log.getEffectiveLevel()
    else:
        log_level = logging.WARNING

    requests_log = logging.getLogger('requests')
    requests_log.setLevel(log_level)

    requests_log = logging.getLogger('urllib3.connectionpool')
    requests_log.setLevel(log_level)


def normalize_options(options):
    normalized = {}
    for key, value in options.items():

        # Add primary variant.
        key = key.strip('--<>')
        normalized[key] = value

        # Add secondary variant.
        key = key.replace('-', '_')
        normalized[key] = value

    return munchify(normalized)
