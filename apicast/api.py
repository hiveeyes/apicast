# -*- coding: utf-8 -*-
# (c) 2020-2021 Andreas Motl <andreas@hiveeyes.org>
# License: GNU Affero General Public License, Version 3
import logging
from typing import List, Dict

from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse, PlainTextResponse

from apicast import __appname__, __version__
from apicast.core import (DwdBeeflightForecast, dwd_copyright, dwd_source,
                          producer_link, producer_name)
from apicast.format import Formatter

app = FastAPI()

log = logging.getLogger(__name__)

dbf = DwdBeeflightForecast()


@app.get("/", response_class=HTMLResponse)
def index():

    appname = f"{__appname__} {__version__}"
    description = "Apicast acquires bee flight forecast information published by Deutscher Wetterdienst (DWD)."

    data_index_items = []
    for location in dbf.get_station_slugs():
        item = f"""
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
        """
        data_index_items.append(item)

    data_index_items_html = "\n".join(data_index_items)

    return f"""
    <html>
        <head>
            <title>{appname}</title>

            <meta name="description"
                content="{description}">
            <meta name="keywords"
                content="honey bee, apis mellifera, flight forecast information, dwd, cdc, deutscher wetterdienst, climate data center, weather, opendata, data acquisition, transformation, export, geospatial, temporal, timeseries, sensor, network, observation, http, rest, api, json, markdown">

            <meta property="og:title" content="{appname}"/>
            <meta property="og:site_name" content="{appname}">
            <meta property="og:description"
                content="{description}"/>
            <meta property="og:url" content="https://apicast.hiveeyes.org/"/>
            <meta property="og:image" content="https://ptrace.hiveeyes.org/2021-03-05_beeswarm_plymouth.jpg"/>
            <meta property="og:image:secure_url" content="https://ptrace.hiveeyes.org/2021-03-05_beeswarm_plymouth.jpg"/>
            <meta property="og:type" content="website"/>

            <meta name="twitter:title" content="{appname}">
            <meta name="twitter:description" content="{description}">
            <meta name="twitter:image" content="https://ptrace.hiveeyes.org/2021-03-05_beeswarm_plymouth.jpg">
            <meta name="twitter:image:alt" content="Bee swarm in Plymouth">
            <meta name="twitter:card" content="summary_large_image">

            <script type='application/ld+json'>{{"@context":"https://schema.org","@type":"WebSite","@id":"#website","url":"https://apicast.hiveeyes.org/","name":"{appname}","logo":"https://ptrace.hiveeyes.org/2021-03-05_beeswarm_plymouth.jpg"}}</script>

        </head>
        <body>
            <h2>About</h2>
            <div style="width: 68%">
                <div style="float: left">
                {description}
                <ul>
                <li>Producer: <a href="{producer_link}">{producer_name}</a></li>
                <li>Source: <a href="{dwd_source}">DWD » Freizeitgärtner » Gartenwetter » Prognose des Bienenfluges</a></li>
                <li>Data copyright: {dwd_copyright}</li>
                </ul>
                </div>
                <div style="float: right">
                    <img src="https://ptrace.hiveeyes.org/2021-03-05_beeswarm_plymouth.jpg" width="200"/>
                </div>
            </div>
            <div style="clear: both"/>

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
    return make_json_response(data=stations, location="germany")


@app.get("/beeflight/stations/germany/locations")
def beeflight_stations_site_slugs():
    slugs = dbf.get_station_slugs()
    return make_json_response(data=slugs, location="germany")


@app.get("/beeflight/forecast/germany/{state}/{station}")
def beeflight_forecast_by_slug(
    state: str,
    station: str,
    format: str = Query(default="json"),
    translate: bool = Query(default=False),
):

    station_slug = f"{state}/{station}"

    try:
        station = dbf.get_station_by_slug(station_slug)
        result = dbf.get_data(station=station).copy()
        if not result.data:
            raise ValueError("No data found or unable to parse")
    except Exception as ex:
        return {"error": str(ex)}

    formatter = Formatter(result)

    if translate:
        formatter.translate()

    if format == "json-machine":
        response = formatter.machinify()

    elif format == "table-markdown":
        return PlainTextResponse(formatter.table_markdown())

    else:
        response = formatter.normalize()

    return make_json_response(data=response, location=station_slug)


def make_json_response(data: List[Dict], location: str = None):
    response = {
        "meta": {
            "source": dwd_source,
            "producer": f"{producer_name} - {producer_link}",
            "copyright": dwd_copyright,
        },
        "location": {
            "slug": location,
        },
        "data": data,
    }
    return response


def start_service(listen_address, reload: bool = False):
    host, port = listen_address.split(":")
    port = int(port)
    from uvicorn.main import run

    run(app="apicast.api:app", host=host, port=port, reload=reload)
