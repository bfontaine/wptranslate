.PHONY: all freeze check covercheck coverhtml

SRC=wptranslate

VENV=./venv
BINPREFIX=$(VENV)/bin/

PIP=$(BINPREFIX)pip

COVERFILE:=.coverage
COVERAGE_REPORT:=report -m

PY_VERSION:=$(subst ., ,$(shell python --version 2>&1 | cut -d' ' -f2))
PY_VERSION_MAJOR:=$(word 1,$(PY_VERSION))
PY_VERSION_MINOR:=$(word 2,$(PY_VERSION))
PY_VERSION_SHORT:=$(PY_VERSION_MAJOR).$(PY_VERSION_MINOR)

ifdef TRAVIS_PYTHON_VERSION
PY_VERSION_SHORT:=$(TRAVIS_PYTHON_VERSION)
endif

all: run

deps:
	$(BINPREFIX)pip install -r requirements.txt
ifeq ($(PY_VERSION_SHORT),2.6)
	$(BINPREFIX)pip install unittest2
endif

freeze: $(VENV)
	$(PIP) freeze >| requirements.txt

$(VENV):
	virtualenv $@

# Tests

check:
	$(BINPREFIX)python tests/test.py

check-versions:
	$(BINPREFIX)tox

covercheck:
	$(BINPREFIX)coverage run --source=$(SRC) tests/test.py
	$(BINPREFIX)coverage $(COVERAGE_REPORT)

coverhtml:
	@make COVERAGE_REPORT=html BINPREFIX=$(BINPREFIX) covercheck
	@echo '--> open htmlcov/index.html'

publish: deps check-versions
	$(BINPREFIX)python setup.py sdist upload
