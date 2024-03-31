===============
Apicast CHANGES
===============


Development
===========

2024-03-31 0.9.0
================
- Add support for Python 3.12
- Dependencies: Update from docopt to docopt-ng
- Fix translation "sehr hoch" => "intensive"
- Add content and copyright attribution to Markdown output

2023-04-09 0.8.6
================
- Tests: Add more test cases to prepare automatic Dependabot updates
- CI: Enable Dependabot notifications
- Update flight intensity states: Add ``hoch`` and ``sehr hoch``
- Update a few dependencies across the board


2023-04-09 0.8.5
================
- Fix typo in ``setup.py``


2023-04-09 0.8.4
================
- Fix HTML parsing. The section title changed to ``Prognose der
  Bienenflugintensität``.
- Use ``apicast/<version>`` as HTTP user agent string
- Add support for Python 3.10 and 3.11


2021-03-05 0.8.3
================
- Fix translation of Markdown output


2021-03-05 0.8.2
================
- Fix HTTP API endpoint for locations


2021-03-05 0.8.1
================
- Fix type hints and missing dependencies


2021-03-05 0.8.0
================
- Adjust scraping machinery to updated upstream interface
- Add software tests
- Improve HTTP API and web interface
- Enable GHA CI
- Update README


2020-06-04 0.7.1
================
- Fix parsing German dates


2020-06-04 0.7.0
================
- Add machine-readable output format ``json-machine``
- Output formatting available via CLI and HTTP API


2020-06-02 0.6.0
================
- Change API URI format again


2020-06-02 0.5.0
================
- Add "robots.txt" to HTTP API


2020-06-02 0.4.0
================
- Improve documentation, naming things
- Use "/beeflight/germany" as API URL prefix for data from DWD
- Clean up session id which slipped into state url
- Add basic TTL cache to prevent hammering the DWD site


2020-06-02 0.3.0
================
- Add HTTP API based on FastAPI


2020-06-02 0.2.0
================
- Convert to Python3
- Add setup.py, README.rst and CHANGES.rst
- Provide ``extract_sites.sh`` through ``apicast beeflight stations``
- Output beeflight forecast in JSON or table format
- Add release tooling


2018-04-13 0.1.0
================
- Initial commit, prototype spike
- Add script for extracting sites from DWD where forecasts are available. Thanks, @thiasB!
