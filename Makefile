# A Makefile for Python packages.
#
# Not something you usually see, I know, but maybe it's the beginning of an
# application CI/CD API. Is it?
#
# In the context of a Python package, I've made the following interpretations:
#
# 	- "build" means packaging the source code into both a Python wheel file and
# 	  a tarball in the dist dir.
# 	- "install" means using pip to install that wheel file, replacing any
# 	  existing installation.
#
# Given those interpretations, it acts like you would expect a Makefile to,
# except for the following caveats:
#
# 	- Builds are done with setuptools and so a setup.py file in the directory
# 	  above the source directory is required, but that's no leap.
# 	- Installs are done with pip and so it is required, but you should be using
# 	  a virtual environment anyway, right?
# 	- Requirement and package installation are tracked using empty target files
# 	  in the $(makedir) directory. [default: ./.make]
# 	- Since there is no good way to remove unused requirements of the package
# 	  during uninstallation, this is not attempted.
#
# Common use cases:
#
# 	- Build and install the package if not installed or src files have changed
# 		- make install
# 	- Install the development requirements and the package in "editable" mode
# 		- make devinstall
# 	- Test the package using tox
# 		- make test
# 	- Generate test coverage information that prints in the terminal and
# 	  creates HTML and XML format files.
# 		- make coverage
# 	- Publish test coverage infromation to coveralls (the project must be
# 	  registered and the token must be in the COVERALLS_REPO_TOKEN env var)
# 	  	- make coveralls
# 	- Release a new final version by pushing a new tag to GitHub and uploading
# 	  the dist files to PyPi (the project must be registered at PyPi and you
# 	  must have PyPi credentials available or in the PYPI_USER and PYPI_PASS
# 	  env vars).
# 	  	- make release
#

# This should be your package name.
pkg = dmdj
# This (after the $(pkg) part) should be a list of your requirements.
reqs = $(pkg) django>=1.7,<1.11
# This (after the $(pkg)-dev part) should be a list of your dev requirements.
devreqs = $(pkg)-dev django>=1.7,<1.11 wheel twine tox pytest coverage \
          pytest-cov coveralls

# There should be no need to change these, but they're configurable in case.
srcdir = ./$(pkg)
builddir = ./build
distdir = ./dist
makedir = ./.make
PYTHON = python
PIP = pip

# Get the git commit sha for the package version, set to 0 if fails.
GIT_SHA = $(or $(shell cd $(srcdir) && git log -1 --pretty=format:"%h"),0)
# The sha needs to be "exported" for later setup.py calls that re-get the ver.
export GIT_SHA
# The build number should be in the BUILD_NUM env var, otherwise set to 0.
BUILD_NUM ?= 0

# Get the ver from the package.
ver := $(shell GIT_SHA=$(GIT_SHA) $(PYTHON) -c \
         "from $(pkg) import get_version; print(get_version())")

# Define a recursive search function.
rwildcard = $(wildcard $1$2)$(foreach d,$(wildcard $1*),$(call rwildcard,$d/,$2))

# List of all *.py src files, changes to which will trigger re-building.
objects = $(call rwildcard,$(srcdir)/,*.py)
# Name of the wheel dist file for this ver.
distfile = $(distdir)/$(pkg)-$(ver)-py2.py3-none-any.whl
# Name of the source tar ball for this ver.
tarball = $(distdir)/$(pkg)-$(ver).tar.gz


# Start of recipes.
#
# Note that the requirements are installed using an implicit $(makedir)/% rule
# and env vars are checked using an implicit guard-% rule.

# Targets that don't represent actual files.
.PHONY: all build dist tar install devinstall uninstall release test check \
        coverage coveralls clean mostlyclean distclean realclean clobber \
        final-version

all: build

build: dist tar

dist: $(distfile)

tar: $(tarball)

# Build the wheel dist file.
$(distfile): $(objects) $(makedir)/wheel
	$(PYTHON) $(srcdir)/../setup.py bdist_wheel --universal \
        --bdist-dir $(builddir) --dist-dir $(distdir)

# Build the source tar ball and remove the egg-info dir afterwards.
$(tarball): $(objects)
	$(PYTHON) $(srcdir)/../setup.py sdist --dist-dir $(distdir)
	@ rm -rf $(pkg).egg-info

# Install the package and it's requirements.
install: $(addprefix $(makedir)/,$(devreqs))

# Install the package from the wheel dist file instead of directly from source.
# Remove the devinstall marker file if it exists.
$(makedir)/$(pkg): $(distfile)
	$(PIP) install --upgrade --force-reinstall --no-deps $(distfile)
	@ touch $(makedir)/$(pkg)
	@ rm -f $(makedir)/$(pkg)-dev

# Install the package as "editable" and the dev requirements.
devinstall: $(addprefix $(makedir)/,$(devreqs))

# Install the package as editable. If the install marker file exists, uninstall
# the package first. Remove the install marker file afterwards.
$(makedir)/$(pkg)-dev:
ifneq ($(wildcard $(makedir)/$(pkg)),)
	$(PIP) uninstall -y $(pkg)
endif
	$(PIP) install --no-deps --editable $(srcdir)/..
	@ touch $(makedir)/$(pkg)-dev
	@ rm -f $(makedir)/$(pkg)

# Uninstall the package and remove either the install or devinstall marker.
uninstall:
	$(PIP) uninstall -y $(pkg)
	@ rm -f $(makedir)/$(pkg) $(makedir)/$(pkg)-dev

# Set up the auth arguments for the PyPi upload command if the respective env
# vars are defined. Without these arguments, twine interactively prompts for
# auth. This is mostly useful for CI/CD workflows.
ifdef PYPI_USER
user_arg := -u "$(PYPI_USER)"
endif
ifdef PYPI_PASS
pass_arg := -p "$(PYPI_PASS)"
endif

# If the version is final, push a new tag to github and upload to PyPi.
# You need to have a PyPi account with available credentials and the package
# needs to be registered already.
release: final-version $(makedir)/twine $(distfile) $(tarball)
	git tag -a "$(ver)" -m "Release of version $(ver)"
	git push --tags
	twine upload $(user_arg) $(pass_arg) dist/*

# Test the package using tox. Make sure your tox.ini file is set up.
test check: $(makedir)/tox $(makedir)/pytest
	tox $(srcdir)

# Generate coverage reports and print coverage to the screen.
coverage: $(makedir)/pytest-cov
	pytest --cov-report=term-missing --cov-report=xml --cov-report=html \
        --cov=$(pkg) $(pkg)

# Push the coverage report to coveralls. The project needs to be registered
# there and the token needs to be in the COVERALLS_REPO_TOKEN env var.
coveralls: guard-COVERALLS_REPO_TOKEN $(makedir)/coveralls coverage
	coveralls

# Remove build and dist artifacts. If things have gone as intended, only the
# dist dir should actually exist.
clean mostlyclean:
	rm -rf $(distdir) $(builddir) $(pkg).egg-info

# Remove additional artifacts: the coverage reports and tracking files.
distclean realclean clobber: clean
	rm -rf htmlcov coverage.xml $(makedir)

# Check if the length of $(ver) is exactly 5 characters, meaning it's final.
final-version:
ifneq ($(strip $(shell printf "$(ver)" | awk '{print length}')), 5)
	$(error "Don't release non-final version $(ver)!")
endif

# Install the "%" python dependency. Creates an empty target file in $(makedir)
# to track the installation time.
$(makedir)/%: | $(makedir)
	$(PIP) install -U "$*"
	@ touch "$@"

# Create the tracking file directory.
$(makedir):
	@ mkdir -p $(makedir)

# Cause an error if the "%" environment variable isn't set.
guard-%:
	$(if $(shell printf "${$*}"),	,\
      $(error "Environment variable $* must be set!"))

# Print the "%" variable for debugging.
print-%:
	@ echo $*=$($*)
