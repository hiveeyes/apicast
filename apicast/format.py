# -*- coding: utf-8 -*-
# (c) 2020 Andreas Motl <andreas@hiveeyes.org>
import io
from contextlib import redirect_stdout

import tabulate
from datetime import datetime
from dateutil.parser import parse as parsedate


class Formatter:
    """
    Die Bedingungen für den Bienenflug werden in 5 Intensitätsstufen angegeben
    (kein - gering - mittel - stark - intensiv).

    -- https://www.dwd.de/DE/fachnutzer/freizeitgaertner/dokumentation/gw_bienenflug
    """

    LABEL_MAP = {
        'Datum': 'date',

        'morgens': 'morning',
        'mittags': 'noon',
        'abends': 'evening',

        'kein': 'no',
        'gering': 'low',
        'mittel': 'medium',
        'stark': 'strong',
        'intensiv': 'intensive',
    }

    STRENGTH_MACHINE_MAP = {
        'no': 0,
        'low': 1,
        'medium': 2,
        'strong': 3,
        'intensive': 4,
    }

    def __init__(self, result):
        self.result = result
        self.data = result["data"]

    def translate(self):
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
                if key == 'date':
                    value += str(datetime.now().year)
                    value = parsedate(value, fuzzy=True).strftime('%Y-%m-%d')
                elif value in self.STRENGTH_MACHINE_MAP.keys():
                    value = self.STRENGTH_MACHINE_MAP[value]
                item[key] = value
        return data

    def table_markdown(self):
        with io.StringIO() as buffer, redirect_stdout(buffer):

            # Report about weather station / observation location
            print(u'### Prognose des Bienenfluges in {}'.format(self.result['station']))
            print()

            # Output forecast data
            print(tabulate.tabulate(self.data[1:], headers=self.data[0], showindex=False, tablefmt='pipe'))

            return buffer.getvalue()
