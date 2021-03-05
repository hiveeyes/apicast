# =============
# Configuration
# =============

$(eval venv         := .venv)
$(eval pip          := $(venv)/bin/pip)
$(eval python       := $(venv)/bin/python)
$(eval pytest       := $(venv)/bin/pytest)
$(eval bumpversion  := $(venv)/bin/bumpversion)
$(eval twine        := $(venv)/bin/twine)

$(eval apicast      := $(venv)/bin/apicast)


# =====
# Setup
# =====

# Setup Python virtualenv
setup-virtualenv:
	@test -e $(python) || python3 -m venv $(venv)

# Install requirements for development.
virtualenv-dev: setup-virtualenv
	@test -e $(apicast) || $(pip) install --upgrade --editable=.[service]
	@test -e $(pytest) || $(pip) install --upgrade --requirement=requirements-test.txt

install-releasetools: setup-virtualenv
	@$(pip) install --quiet --requirement requirements-release.txt --upgrade


# =======
# Release
# =======

# Release this piece of software.
# Uses the fine ``bumpversion`` utility.
#
# Synopsis::
#
#    make release bump={patch,minor,major}

release: bumpversion push sdist pypi-upload

bumpversion: install-releasetools
	@$(bumpversion) $(bump)

push:
	git push && git push --tags

sdist:
	@$(python) setup.py sdist

pypi-upload: install-releasetools
	twine upload --skip-existing --verbose dist/*.tar.gz


# ==============
# Software tests
# ==============

.PHONY: test
pytest: virtualenv-dev

	@# Run pytest.
	$(pytest) test -vvv

test: pytest

test-coverage: virtualenv-dev
	$(nosetests) \
		--with-doctest --doctest-tests --doctest-extension=rst \
		--with-coverage --cover-package=apicast --cover-tests \
		--cover-html --cover-html-dir=coverage/html --cover-xml --cover-xml-file=coverage/coverage.xml
