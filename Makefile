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

# Install requirements for releasing.
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
test: virtualenv-dev
	$(pytest)
