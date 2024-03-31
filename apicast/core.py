# -*- coding: utf-8 -*-
# (c) 2018-2021 Andreas Motl <andreas@hiveeyes.org>
# License: GNU Affero General Public License, Version 3
"""
Apicast acquires bee flight forecast information published by Deutscher Wetterdienst (DWD).

Parse information about "Gartenwetter » Bienenflug"
from https://www.dwd.de/DE/leistungen/biene_flug/bienenflug.html.

See also https://community.hiveeyes.org/t/dwd-prognose-bienenflug/787
"""

import dataclasses
from typing import List

import requests
import ttl_cache
from bs4 import BeautifulSoup
from html_table_extractor.extractor import Extractor
from slugify import slugify

from apicast import __appname__, __version__

user_agent = f"{__appname__}/{__version__}"
dwd_copyright = "© Deutscher Wetterdienst (DWD)"
dwd_name = "DWD Agricultural Meteorology Department"
dwd_link = "https://www.dwd.de/DE/leistungen/biene_flug/bienenflug.html"
apicast_name = "Hiveeyes Apicast"
apicast_link = "https://github.com/hiveeyes/apicast"


@dataclasses.dataclass
class State:
    label: str
    identifier: str


@dataclasses.dataclass
class Station:
    state: State
    label: str
    identifier: str
    slug: str


@dataclasses.dataclass
class Result:
    station: Station
    station_name: str
    data: List
    footnote: str

    def copy(self):
        return Result(**dataclasses.asdict(self))


class DwdBeeflightForecast:
    baseurl = "https://www.dwd.de/DE/leistungen/biene_flug/bienenflug.json?cl2Categories_LeistungsId=bienenflug"

    session = requests.Session()
    session.headers["User-Agent"] = user_agent

    @ttl_cache(60 * 60 * 24)
    def get_states(self) -> List[State]:
        states: List[State] = []

        # Request federal states.
        response = self.session.get(
            self.baseurl, params={"view": "renderJson", "cl2Categories_Bundesland": ""}
        )
        data = response.json()
        for item in data["cl2Categories_Bundesland"].values():
            state = State(label=item["label"], identifier=item["val"])

            states.append(state)

        # sites.sort(key=operator.attrgetter("label"))  # noqa: ERA001

        return states

    @ttl_cache(60 * 60 * 24)
    def get_stations(self) -> List[Station]:
        stations: List[Station] = []

        # Request federal states.
        for state in self.get_states():
            # Request sites.
            response = self.session.get(
                self.baseurl,
                params={
                    "view": "renderJson",
                    "cl2Categories_Bundesland": state.identifier,
                    "cl2Categories_Station": "",
                },
            )
            data = response.json()
            for item in data["cl2Categories_Station"].values():
                identifier = item["val"]
                if identifier == "bifl_0000":
                    continue
                label = item["label"]
                station = Station(
                    state=state,
                    label=label,
                    identifier=identifier,
                    slug=f"{slugify(state.label)}/{slugify(label)}",
                )

                stations.append(station)

        # sites.sort(key=operator.attrgetter("label"))  # noqa: ERA001

        return stations

    def get_station_slugs(self) -> List[str]:
        slugs = []
        for station in self.get_stations():
            slugs.append(station.slug)
        slugs.sort()
        return slugs

    def get_station_by_slug(self, slug):
        for station in self.get_stations():
            if station.slug == slug:
                return station
        raise KeyError("No such station")

    @ttl_cache(60 * 60)
    def get_data(self, station: Station) -> Result:
        response = self.session.get(
            self.baseurl,
            params={
                "view": "renderJsonResults",
                "cl2Categories_Bundesland": station.state.identifier,
                "cl2Categories_Station": station.identifier,
            },
        )

        soup = BeautifulSoup(markup=response.content, features="html.parser")

        # Find content section and extract elements.
        headline = soup.find(string="Prognose der Bienenflugintensität")
        if not headline:
            raise ValueError("No forecast available for this station")
        station_name = headline.find_next("section").attrs.get("aria-label")
        table = soup.find("table")

        footnote = soup.find("aside").find("p").text

        # Read HTML table
        data = self.parse_html_table(table)

        # Ready.
        return Result(station=station, station_name=station_name, data=data, footnote=footnote)

    @staticmethod
    def parse_html_table(html):
        extractor = Extractor(html)
        extractor.parse()
        return extractor.return_list()
