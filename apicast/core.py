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
import re
import mechanicalsoup
from munch import Munch
from html_table_extractor.extractor import Extractor


user_agent = u"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36"


def dwd_beeflight_forecast_stations():

    base_url = "https://www.dwd.de/"
    app_path = "DE/fachnutzer/freizeitgaertner/1_gartenwetter/"
    index_url = f"{base_url}{app_path}_node.html"

    browser = mechanicalsoup.StatefulBrowser(user_agent=user_agent)
    page = browser.open(index_url)

    # Find navigation section and extract elements.
    nav_main = page.soup.find(attrs={'class': 'navMain'})
    state_links = nav_main.find_all('a', href=re.compile('.+1_gartenwetter.+'))

    results = []

    for state_link in state_links:
        state_title = state_link['title']
        state_url = f"{base_url}{state_link['href']}"

        state_link_prefix = re.sub('/_node.html.*', '', state_link['href'])
        state_slug = state_link_prefix.replace(app_path, '')

        state = Munch({
            'title': state_title,
            'url': state_url,
            'slug': state_slug,
            'sites': [],
        })

        page = browser.open(state_url)

        nav_main = page.soup.find(attrs={'class': 'navMain'})
        site_links = nav_main.find_all('a', href=re.compile(f'.*{state_link_prefix}.*'))

        for site_link in site_links:
            site_title = site_link['title']
            site_url = f"{base_url}{site_link['href']}"
            site_link_prefix = re.sub('/_node.html.*', '', site_link['href'])
            site_slug = site_link_prefix.replace(app_path, '')
            site = Munch({
                'title': site_title,
                'url': site_url,
                'slug': site_slug,
            })

            state.sites.append(site)

        results.append(state)

    return results


def dwd_beeflight_site_url_by_slug(slug):
    url = f"https://www.dwd.de/DE/fachnutzer/freizeitgaertner/1_gartenwetter/{slug}/_node.html"
    return url


def grok_beeflight_forecast(url):

    # Navigate to HTTP resource.
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
