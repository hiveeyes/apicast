#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
apicast acquires bee flight forecast information published by Deutscher Wetterdienst (DWD)

Parse information about "Gartenwetter » Bienenflug"
from https://www.dwd.de/DE/fachnutzer/freizeitgaertner/1_gartenwetter/_node.html ff.

See also https://community.hiveeyes.org/t/dwd-prognose-bienenflug/787


Prerequisites::

    pip install MechanicalSoup==0.10.0 html-table-extractor==1.3.0 tabulate==0.8.2

Synopsis::

    python apicast.py https://www.dwd.de/DE/fachnutzer/freizeitgaertner/1_gartenwetter/berlin_brandenburg/potsdam/_node.html

"""
import sys
import mechanicalsoup
from html_table_extractor.extractor import Extractor
from tabulate import tabulate


def grok_beeflight_forecast(url):

    # Navigate to HTTP resource
    user_agent = u'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36'
    browser = mechanicalsoup.StatefulBrowser(user_agent=user_agent)
    page = browser.open(url)

    # Find content section and extract elements
    subject = page.soup.find(string=u'Prognose des Bienenfluges')
    station = subject.find_next('br').next.strip()
    table = subject.parent.find_next_sibling('table')
    # TODO: Read table footer "© Deutscher Wetterdienst, erstellt 12.04.2018 04:00 UTC"

    # Read HTML table
    data = parse_html_table(unicode(table))

    # Ready.
    result = {
        'station': station,
        'data': data,
    }
    return result


def parse_html_table(html):
    extractor = Extractor(html)
    extractor.parse()
    return extractor.return_list()


if __name__ == '__main__':

    # Sanity checks
    if len(sys.argv) < 2:
        raise KeyError('Please specify url as single positional argument')
    url = sys.argv[1]

    # Fetch and extract forecast information
    result = grok_beeflight_forecast(url)

    # Report about weather station / observation location
    print
    print u'### Prognose des Bienenfluges in {}'.format(result['station'])
    print

    # Output forecast data
    data = result['data']
    print tabulate(data[1:], headers=data[0], showindex=False, tablefmt='pipe').encode('utf-8')
