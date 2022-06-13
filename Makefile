.PHONY: all tests docs clean init init-deps flake8 pylint

PYTHON_FILES := $(shell find src tests -name '*.py')

all:
	@echo "make dev -- Run DevServer ( http://localhost:8000 )"
	@echo "make tests -- Run all tests"
	@echo "make docs -- Generate documentation"
	@echo "make pylint"
	@echo "make flake8"
	@echo "make venv -- (once) run before all"
	@echo "source venv/bin/activate -- activate virtualenv"

ifndef VIRTUAL_ENV
VIRTUALENV_HELP := Use 'make venv' to automatically create a pre-configured virtualenv.
pip = $(error "No active virtualenv for pip. $(VIRTUALENV_HELP)")
pytest = $(error "No active virtualenv for pytest. $(VIRTUALENV_HELP)")
else
pip = pip
pytest = py.test $(PYTEST_ARGS)
endif

define ERROR
	(echo -en "\nERROR: [$@]: $(1)\n\n" && exit 1)
endef

venv:
	@echo "Creating pre-configured virtualenv ..."
	python3 -m venv ./venv
	./venv/bin/pip install --upgrade pip
	@echo "Use 'source venv/bin/activate' to activate the virtualenv."

init.marker: requirements.txt
	$(pip) install --upgrade -r requirements.txt && touch $@
init: init.marker

init-deps.marker: init.marker requirements-deps.txt
	$(pip) install --upgrade -r requirements-deps.txt && touch $@
init-deps: init-deps.marker

dev: init
	#uvicorn src.main:app --reload
	python3 -m src.main

tests: init-deps init
	python -m pytest -s tests

docs: init-deps init
	sphinx-apidoc -f -o docs/source src/
	$(MAKE) -C docs html

clean:
	rm -f *.marker
	$(MAKE) -C docs clean


define FLAKE8
	@echo "Running flake8 code checks ..."
	@flake8 $(1) || $(call ERROR, "Flake8 static code checks failed!")
endef

flake8: init-deps
	$(call FLAKE8,$(PYTHON_FILES))

define PYLINT
	@echo "Running pylint ..."
	@pylint --reports=no -f msvs -j5 $(1) || $(call ERROR, "Pylint static code checks failed!")
endef

pylint: init-deps
	$(call PYLINT, $(PYTHON_FILES))
