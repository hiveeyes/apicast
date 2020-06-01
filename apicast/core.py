# -*- coding: utf-8 -*-
# (c) 2018-2020 Andreas Motl <andreas@hiveeyes.org>
"""
apicast acquires bee flight forecast information published by Deutscher Wetterdienst (DWD)

Parse information about "Gartenwetter » Bienenflug"
from https://www.dwd.de/DE/fachnutzer/freizeitgaertner/1_gartenwetter/_node.html ff.

See also https://community.hiveeyes.org/t/dwd-prognose-bienenflug/787


Synopsis::

    apicast --url https://www.dwd.de/DE/fachnutzer/freizeitgaertner/1_gartenwetter/berlin_brandenburg/potsdam/_node.html

"""
import mechanicalsoup
from html_table_extractor.extractor import Extractor


def grok_beeflight_forecast(url):

    # Navigate to HTTP resource.
    user_agent = u'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36'
    browser = mechanicalsoup.StatefulBrowser(user_agent=user_agent)
    page = browser.open(url)

    # Find content section and extract elements.
    subject = page.soup.find(string=u'Prognose des Bienenfluges')
    station = subject.find_next('br').next.strip()
    table = subject.parent.find_next_sibling('table')
    # TODO: Read table footer "© Deutscher Wetterdienst, erstellt 12.04.2018 04:00 UTC"

    # Read HTML table
    data = parse_html_table(table)

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
