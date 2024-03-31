import marko
import pytest

from apicast.core import Result, State, Station
from apicast.format import Formatter

sample_result = Result(
    station=Station(
        state=State(label="Brandenburg", identifier="bifl_bl04"),
        label="Potsdam",
        identifier="bifl_0021",
        slug="brandenburg/potsdam",
    ),
    station_name="Potsdam",
    data=[
        ["Datum", "morgens", "mittags", "abends"],
        ["Sa 30.03.", "mittel", "sehr hoch", "hoch"],
        ["So 31.03.", "mittel", "hoch", "hoch"],
        ["Mo 01.04.", "mittel", "hoch", "mittel"],
    ],
    footnote="© Deutscher Wetterdienst, erstellt 30.03.2024 05:00 UTC. Alle Angaben ohne Gewähr!",
)

markdown_reference = """
### Prognose des Bienenfluges in Potsdam

| Datum     | morgens   | mittags   | abends   |
|:----------|:----------|:----------|:---------|
| Sa 30.03. | mittel    | sehr hoch | hoch     |
| So 31.03. | mittel    | hoch      | hoch     |
| Mo 01.04. | mittel    | hoch      | mittel   |

© Deutscher Wetterdienst (DWD)
[DWD Agricultural Meteorology Department] • [Hiveeyes Apicast]

[DWD Agricultural Meteorology Department]: https://www.dwd.de/DE/leistungen/biene_flug/bienenflug.html
[Hiveeyes Apicast]: https://github.com/hiveeyes/apicast
""".lstrip()


@pytest.fixture
def formatter() -> Formatter:
    return Formatter(sample_result)


def test_format_basic(formatter: Formatter):
    assert formatter.title == "### Prognose des Bienenfluges in Potsdam"
    assert len(formatter.data) == 4


def test_format_normalize(formatter: Formatter):
    assert formatter.normalize() == [
        {"Datum": "Sa 30.03.", "morgens": "mittel", "mittags": "sehr hoch", "abends": "hoch"},
        {"Datum": "So 31.03.", "morgens": "mittel", "mittags": "hoch", "abends": "hoch"},
        {"Datum": "Mo 01.04.", "morgens": "mittel", "mittags": "hoch", "abends": "mittel"},
    ]


def test_format_machinify(formatter: Formatter):
    assert formatter.machinify() == [
        {"date": "2024-03-30", "evening": 3, "morning": 2, "noon": 4},
        {"date": "2024-03-31", "evening": 3, "morning": 2, "noon": 3},
        {"date": "2024-04-01", "evening": 2, "morning": 2, "noon": 3},
    ]


def test_format_translate(formatter: Formatter):
    formatter.translate()
    assert formatter.data == [
        ["date", "morning", "noon", "evening"],
        ["Sa 30.03.", "medium", "intensive", "strong"],
        ["So 31.03.", "medium", "strong", "strong"],
        ["Mo 01.04.", "medium", "strong", "medium"],
    ]


def test_format_markdown(formatter: Formatter):
    markdown = formatter.table_markdown()
    assert markdown_reference == markdown
    assert "Datum" in markdown
    assert "sehr strong" not in markdown

    html = marko.convert(markdown)
    assert html.startswith("<h3>Prognose des Bienenfluges in Potsdam</h3>")
