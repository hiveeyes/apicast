# -*- coding: utf-8 -*-
# (c) 2020 Andreas Motl <andreas@terkin.org>
# License: GNU Affero General Public License, Version 3
import logging
from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse

from apicast import __appname__, __version__
from apicast.core import dwd_beeflight_forecast_stations, dwd_beeflight_forecast_stations_site_slugs, \
    dwd_beeflight_site_url_by_slug, grok_beeflight_forecast

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
            {about}
            <hr/>
            Index
            <ul>
            <li><a href="beeflight/stations">List of federal states / sites</a></li>
            <li><a href="beeflight/stations/site-slugs">List of site slugs</a></li>
            </ul>
            <hr/>
            Examples
            <ul>
            <li><a href="beeflight/forecast/berlin_brandenburg/potsdam">Bee flight forecast for "berlin_brandenburg/potsdam"</a></li>
            <li><a href="beeflight/forecast/bayern/regensburg">Bee flight forecast for "bayern/regensburg"</a></li>
            </ul>
        </body>
    </html>
    """


@app.get("/beeflight/stations")
def beeflight_stations():
    stations = dwd_beeflight_forecast_stations()
    return stations


@app.get("/beeflight/stations/site-slugs")
def beeflight_stations_site_slugs():
    slugs = dwd_beeflight_forecast_stations_site_slugs()
    return slugs


@app.get("/beeflight/forecast/{state}/{site}")
def beeflight_forecast_by_slug(state: str, site: str):
    station_slug = f"{state}/{site}"

    try:
        url = dwd_beeflight_site_url_by_slug(station_slug)
        result = grok_beeflight_forecast(url)
        data = result['data']
        if not data:
            raise ValueError('No data found or unable to parse')
    except Exception as ex:
        return {'error': str(ex)}

    result = []
    for item in data[1:]:
        item = dict(zip(data[0], item))
        result.append(item)

    return result


def start_service(listen_address):
    host, port = listen_address.split(':')
    port = int(port)
    from uvicorn.main import run
    run(app='apicast.api:app', host=host, port=port, reload=True)
