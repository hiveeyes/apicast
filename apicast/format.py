# -*- coding: utf-8 -*-
# (c) 2020-2021 Andreas Motl <andreas@hiveeyes.org>
# License: GNU Affero General Public License, Version 3
import io
from contextlib import redirect_stdout
from copy import deepcopy
from datetime import datetime

import tabulate
from dateparser import parse as parsedate

from apicast.core import apicast_link, apicast_name, dwd_copyright, dwd_link, dwd_name


class Formatter:
    """
    Die Bedingungen für den Bienenflug werden in 5 Intensitätsstufen angegeben
    (kein - gering - mittel - stark - intensiv).

    Die Flugaktivität reicht von geringer, über mittlerer und hoher bis sehr hoher Flugaktivität.

    - https://www.dwd.de/DE/fachnutzer/landwirtschaft/dokumentationen/allgemein/bienenflug_doku.html
    - https://www.dwd.de/DE/fachnutzer/landwirtschaft/dokumentationen/isabel/meinagrar_bienenflug.html?nn=629500
    """

    LABEL_MAP = {
        "Datum": "date",
        "morgens": "morning",
        "mittags": "noon",
        "abends": "evening",
        "kein": "no",
        "gering": "low",
        "mittel": "medium",
        "stark": "strong",
        "intensiv": "intensive",
        # Added 2023
        # https://github.com/hiveeyes/apicast/issues/4
        "sehr hoch": "intensive",
        "hoch": "strong",
    }

    STRENGTH_MACHINE_MAP = {
        "no": 0,
        "low": 1,
        "medium": 2,
        "strong": 3,
        "intensive": 4,
    }

    def __init__(self, result):
        self.result = deepcopy(result)
        self.data = self.result.data
        self.title = "### Prognose des Bienenfluges in {}".format(self.result.station_name)

    def translate(self):
        self.title = "### Beeflight forecast for {}".format(self.result.station_name)
        for item in self.data:
            for index, slot in enumerate(item):
                for key, value in self.LABEL_MAP.items():
                    slot = slot.replace(key, value)
                item[index] = slot
        return self

    def normalize(self):
        result = []
        for item in self.data[1:]:
            item = dict(zip(self.data[0], item))
            result.append(item)
        return result

    def machinify(self):
        self.translate()
        data = self.normalize()
        for item in data:
            for key, value in item.items():
                if key == "date":
                    value += str(datetime.now().year)
                    value = parsedate(value).strftime("%Y-%m-%d")
                elif value in self.STRENGTH_MACHINE_MAP.keys():
                    value = self.STRENGTH_MACHINE_MAP[value]
                item[key] = value
        return data

    # ruff: noqa: T201
    def table_markdown(self):
        with io.StringIO() as buffer, redirect_stdout(buffer):
            # Report about weather station / observation location
            print(self.title)
            print()

            # Output forecast data
            print(
                tabulate.tabulate(
                    self.data[1:],
                    headers=self.data[0],
                    showindex=False,
                    tablefmt="pipe",
                )
            )

            print()
            print(
                f"""
{dwd_copyright}
[{dwd_name}] • [{apicast_name}]

[{dwd_name}]: {dwd_link}
[{apicast_name}]: {apicast_link}
""".strip()
            )

            return buffer.getvalue()
