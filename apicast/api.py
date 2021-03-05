# -*- coding: utf-8 -*-
# (c) 2020-2021 Andreas Motl <andreas@hiveeyes.org>
# License: GNU Affero General Public License, Version 3
import logging

from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse, PlainTextResponse

from apicast import __appname__, __version__
from apicast.core import dwd_source, dwd_copyright, producer_name, producer_link, DwdBeeflightForecast
from apicast.format import Formatter

app = FastAPI()

log = logging.getLogger(__name__)

dbf = DwdBeeflightForecast()


@app.get("/", response_class=HTMLResponse)
def index():
    appname = f'{__appname__} {__version__}'
    about = 'Apicast acquires bee flight forecast information published by Deutscher Wetterdienst (DWD).'

    data_index_items = []
    for location in dbf.get_station_slugs():
        item = f'''
            <li>
                <div style="float: left">
                Forecast for {location}
                </div>
                <div style="float: right">
                German:
                    <a href="beeflight/forecast/germany/{location}?translate=false&format=json">[JSON]</a>
                    <a href="beeflight/forecast/germany/{location}?translate=false&format=table-markdown">[Markdown]</a>
                English:
                    <a href="beeflight/forecast/germany/{location}?translate=true&format=json">[JSON]</a>
                    <a href="beeflight/forecast/germany/{location}?translate=true&format=table-markdown">[Markdown]</a>

                Machine:
                    <a href="beeflight/forecast/germany/{location}?format=json-machine">[JSON]</a>
                </div>
                <div style="clear: both"/>
            </li>
        '''
        data_index_items.append(item)

    data_index_items_html = "\n".join(data_index_items)

    return f"""
    <html>
        <head>
            <title>{appname}</title>
        </head>
        <body>
            <h3>About</h3>
            {about}
            <ul>
            <li>Source: <a href="{dwd_source}">DWD » Freizeitgärtner » Gartenwetter » Prognose des Bienenfluges</a></li>
            <li>Producer: <a href="{producer_link}">{producer_name}</a></li>
            <li>Data copyright: {dwd_copyright}</li>
            </ul>
            <h3>Location index</h3>
            <ul>
            <li><a href="beeflight/stations/germany">List of federal states / stations</a></li>
            <li><a href="beeflight/stations/germany/locations">List of location slugs</a></li>
            </ul>
            <h3>Data index</h3>
            <ul style="width: 65%">
            {data_index_items_html}
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
    stations = dbf.get_stations()
    return make_json_response(stations)


@app.get("/beeflight/stations/germany/locations")
def beeflight_stations_site_slugs():
    slugs = dbf.get_station_slugs()
    return make_json_response(slugs)


@app.get("/beeflight/forecast/germany/{state}/{station}")
def beeflight_forecast_by_slug(state: str, station: str, format: str = Query(default='json'), translate: bool = Query(default=False)):

    station_slug = f"{state}/{station}"

    try:
        station = dbf.get_station_by_slug(station_slug)
        result = dbf.get_data(station=station).copy()
        if not result.data:
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

    return make_json_response(location=station_slug, data=response)


def make_json_response(location: str, data: list[dict]):
    response = {
        'meta': {
            'source': dwd_source,
            'producer': f'{producer_name} - {producer_link}',
            'copyright': dwd_copyright,
        },
        'location': {
            'slug': location,
        },
        'data': data,
    }
    return response


def start_service(listen_address):
    host, port = listen_address.split(':')
    port = int(port)
    from uvicorn.main import run
    run(app='apicast.api:app', host=host, port=port, reload=True)
