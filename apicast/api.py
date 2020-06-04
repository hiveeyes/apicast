# -*- coding: utf-8 -*-
# (c) 2020 Andreas Motl <andreas@terkin.org>
# License: GNU Affero General Public License, Version 3
import logging
from copy import deepcopy

from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse, PlainTextResponse

from apicast import __appname__, __version__
from apicast.core import dwd_beeflight_forecast_stations, dwd_beeflight_forecast_stations_site_slugs, \
    dwd_beeflight_site_url_by_slug, dwd_beeflight_forecast_data, dwd_source, dwd_copyright, producer_name, producer_link
from apicast.format import Formatter

app = FastAPI()

log = logging.getLogger(__name__)


@app.get("/", response_class=HTMLResponse)
def index():
    appname = f'{__appname__} {__version__}'
    about = 'Apicast acquires bee flight forecast information published by Deutscher Wetterdienst (DWD).'
    return f"""
    <html>
        <head>
            <title>{appname}</title>
        </head>
        <body>
            <h3>About</h3>
            {about}
            <ul>
            <li>Source: DWD » Freizeitgärtner » Gartenwetter - <a href="{dwd_source}">{dwd_source}</a></li>
            <li>Producer: {producer_name} - <a href="{producer_link}">{producer_link}</a></li>
            <li>Data copyright: {dwd_copyright}</li>
            </ul>
            <h3>Index</h3>
            <ul>
            <li><a href="beeflight/stations/germany">List of federal states / sites</a></li>
            <li><a href="beeflight/stations/germany/site-slugs">List of site slugs</a></li>
            </ul>
            <h3>Examples</h3>
            <ul>
            <li><a href="beeflight/forecast/germany/berlin_brandenburg/potsdam">Bee flight forecast for "berlin_brandenburg/potsdam"</a></li>
            <li><a href="beeflight/forecast/germany/bayern/regensburg">Bee flight forecast for "bayern/regensburg"</a></li>
            </ul>
        </body>
    </html>
    """


@app.get("/robots.txt", response_class=PlainTextResponse)
def robots():
    return f"""
User-agent: *
Disallow: /beeflight/
    """.strip()


@app.get("/beeflight/stations/germany")
def beeflight_stations():
    stations = dwd_beeflight_forecast_stations()
    return make_json_response(stations)


@app.get("/beeflight/stations/germany/site-slugs")
def beeflight_stations_site_slugs():
    slugs = dwd_beeflight_forecast_stations_site_slugs()
    return make_json_response(slugs)


@app.get("/beeflight/forecast/germany/{state}/{site}")
def beeflight_forecast_by_slug(state: str, site: str, format: str = Query(default='json'), translate: bool = Query(default=False)):
    station_slug = f"{state}/{site}"

    try:
        url = dwd_beeflight_site_url_by_slug(station_slug)
        result = deepcopy(dwd_beeflight_forecast_data(url))
        data = result['data']
        if not data:
            raise ValueError('No data found or unable to parse')
    except Exception as ex:
        return {'error': str(ex)}

    formatter = Formatter(result)

    if translate:
        formatter.translate()

    if format == 'json-machine':
        response = formatter.machinify()

    elif format == 'table-markdown':
        return PlainTextResponse(formatter.table_markdown())

    else:
        response = formatter.normalize()

    return make_json_response(response)


def make_json_response(data):
    response = {
        'meta': {
            'source': dwd_source,
            'copyright': dwd_copyright,
            'producer': f'{producer_name} - {producer_link}',
        },
        'data': data,
    }
    return response


def start_service(listen_address):
    host, port = listen_address.split(':')
    port = int(port)
    from uvicorn.main import run
    run(app='apicast.api:app', host=host, port=port, reload=True)
