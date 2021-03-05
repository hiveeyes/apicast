import dataclasses

from datadiff.tools import assert_equal

from apicast.core import DwdBeeflightForecast

dbf = DwdBeeflightForecast()


def test_get_states():

    states = dbf.get_states()
    bavaria = [state for state in states if state.identifier == "bifl_bl02"][0]

    assert_equal(
        dataclasses.asdict(bavaria),
        {
            "label": "Bayern",
            "identifier": "bifl_bl02",
        },
    )


def test_get_stations():

    stations = dbf.get_stations()
    bavaria_hof = [
        station for station in stations if station.identifier == "bifl_0042"
    ][0]
    berlin_tempelhof = [
        station for station in stations if station.identifier == "bifl_0019"
    ][0]

    assert_equal(
        dataclasses.asdict(bavaria_hof),
        {
            "label": "Hof",
            "identifier": "bifl_0042",
            "slug": "bayern/hof",
            "state": {
                "label": "Bayern",
                "identifier": "bifl_bl02",
            },
        },
    )

    assert_equal(
        dataclasses.asdict(berlin_tempelhof),
        {
            "label": "Berlin-Tempelhof",
            "identifier": "bifl_0019",
            "slug": "berlin/berlin-tempelhof",
            "state": {
                "label": "Berlin",
                "identifier": "bifl_bl03",
            },
        },
    )
