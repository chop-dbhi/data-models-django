# Get the short git sha using a shell command and export it.
GIT_SHA := $(shell git log -1 --pretty=format:"%h")
export GIT_SHA
# Default the build number to 0, if its not in the env.
BUILD_NUM ?= 0
# Get the version number.
ver := $(shell GIT_SHA=$(GIT_SHA) python -c \
		 "from dmdj import get_version; print(get_version())")
# Set of object files to watch for changes.
objects = $(wildcard dmdj/*.py)
# Wheel dist file.
wheel_dist := dist/dmdj-$(ver)-py2.py3-none-any.whl
# Source dist file.
src_dist := dist/dmdj-$(ver).tar.gz
# Set up for twine upload command.
ifdef PYPI_USER
user_arg := -u "$(PYPI_USER)"
endif
ifdef PYPI_PASS
pass_arg := -p "$(PYPI_PASS)"
endif

all: install

install: .make/dmdj

.make/dmdj: $(wheel_dist) $(objects)
	pip install -I $(wheel_dist)
	@ touch .make/dmdj

build: $(wheel_dist) $(src_dist)

build-wheel: $(wheel_dist)

build-src: $(src_dist)

$(wheel_dist): $(objects) .make/wheel
	python setup.py bdist_wheel --universal

$(src_dist): $(objects)
	python setup.py sdist

build-install: .make/wheel

release: final-version .make/twine build
	git tag -a "$(ver)" -m "Release of version $(ver)"
	git push --tags
	twine upload $(user_arg) $(pass_arg) dist/*

release-install: .make/twine

final-version:
ifneq ($(strip $(shell printf $(ver) | wc -c)), 5)
	$(error "Don't release non-final version $(ver)!")
endif

test: .make/tox .make/pytest
	tox

test-install: .make/tox .make/pytest

coveralls: guard-COVERALLS_REPO_TOKEN .make/coveralls coverage.xml
	coveralls

coveralls-install: .make/coveralls

coverage: .make/pytest-cov
	pytest --cov-report=term-missing --cov-report=xml --cov-report=html --cov=dmdj

coverage.xml: .make/pytest-cov $(objects)
	pytest --cov-report=xml --cov=dmdj

htmlcov: .make/pytest-cov $(objects)
	pytest --cov-report=html --cov=dmdj

coverage-install: .make/pytest-cov

clean:
	rm -rf build dist htmlcov dmdj.egg-info coverage.xml .make

.make/%: | .make
	pip install -U $*
	@ touch $@

.make:
	@ mkdir -p .make

guard-%:
	@ if [ "${$*}" = "" ]; then \
		echo "Environment variable $* must be set!"; \
		exit 1; \
	fi

.PHONY: all install build build-install release release-install final-version \
		test test-install coveralls coveralls-install coverage \
		coverage-install clean
