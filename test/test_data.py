import dataclasses

import pytest
from datadiff.tools import assert_equal

from apicast.core import DwdBeeflightForecast, State, Station

dbf = DwdBeeflightForecast()


@pytest.mark.data
def test_get_data_success():
    stations = dbf.get_stations()
    bavaria_hof = [station for station in stations if station.identifier == "bifl_0042"][0]

    data_hof = dbf.get_data(station=bavaria_hof)

    data = data_hof.data
    assert_equal(data[0], ["Datum", "morgens", "mittags", "abends"])

    footnote = data_hof.footnote
    assert "© Deutscher Wetterdienst, erstellt" in footnote
    assert "Alle Angaben ohne Gewähr!" in footnote

    data_hof.data = None
    data_hof.footnote = None

    assert_equal(
        dataclasses.asdict(data_hof),
        {
            "station": {
                "state": {"label": "Bayern", "identifier": "bifl_bl02"},
                "label": "Hof",
                "identifier": "bifl_0042",
                "slug": "bayern/hof",
            },
            "station_name": "Hof",
            "data": None,
            "footnote": None,
        },
    )


@pytest.mark.data
def test_get_data_invalid_station():
    station = Station(
        state=State(label="Nordrhein-Westfalen", identifier="bifl_bl999"),
        label="Bielefeld",
        identifier="bifl_bl999",
        slug="nordrhein-westfalen/bielefeld",
    )
    with pytest.raises(ValueError) as ex:
        dbf.get_data(station=station)
    assert ex.match("No forecast available for this station")


@pytest.mark.data
def test_get_data_copy():
    stations = dbf.get_stations()
    bavaria_hof = [station for station in stations if station.identifier == "bifl_0042"][0]

    data_hof = dbf.get_data(station=bavaria_hof)
    data_hof_copy = data_hof.copy()

    assert id(data_hof) != id(data_hof_copy)
