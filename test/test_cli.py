import json
import shlex
import sys

import marko

from apicast.cli import run


def test_cli_stations(capsys):
    """
    CLI test: Verify reporting about "stations slugs" works.
    """
    command = "apicast beeflight stations --slugs"
    sys.argv = shlex.split(command)

    run()

    out, err = capsys.readouterr()
    assert "brandenburg/potsdam" in out

    items = out.splitlines()
    assert len(items) > 50, "Something went wrong, there should be at least 50 results"


def test_cli_data_json_human(capsys):
    """
    CLI test: Verify reporting about "beeflight forecast" works.
    This report contains human-readable labels.
    """
    command = "apicast beeflight forecast --station=brandenburg/potsdam"
    sys.argv = shlex.split(command)

    run()

    out, err = capsys.readouterr()
    data = json.loads(out)

    assert len(data) == 3, "Something went wrong, the data response should have three items"


def test_cli_data_json_machine(capsys):
    """
    CLI test: Verify reporting about "beeflight forecast" works.
    This report contains machine-readable labels.
    """
    command = "apicast beeflight forecast --station=brandenburg/potsdam --format=json-machine"
    sys.argv = shlex.split(command)

    run()

    out, err = capsys.readouterr()
    data = json.loads(out)

    assert len(data) == 3, "Something went wrong, the data response should have three items"


def test_cli_data_markdown(capsys):
    """
    CLI test: Verify reporting about "beeflight forecast" works.
    This report should yield a Markdown table.
    """
    command = "apicast beeflight forecast --station=brandenburg/potsdam --format=table-markdown"
    sys.argv = shlex.split(command)

    run()

    out, err = capsys.readouterr()
    html = marko.convert(out)

    assert html.startswith("<h3>Prognose des Bienenfluges in Potsdam</h3>")
