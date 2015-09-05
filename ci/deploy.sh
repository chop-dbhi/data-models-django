#!/bin/bash

DIRNAME="$(dirname $0)"
DIRNAME="$( cd ${DIRNAME} && pwd )"
cd "${DIRNAME}/../"
VERSION="$(${DIRNAME}/version.sh)"

# If final version...
if [ ${#VERSION} -lt 6 ]; then

    echo "Creating GitHub release."
    git config --global user.email "aaron0browne@gmail.com"
    git config --global user.name "Aaron Browne"
    git tag -a "${VERSION}" -m "Release of version ${VERSION}"
    git push --tags

    echo "Uploading package to PyPi."
    pip install wheel twine
    sed -e "s/<PYPI_USER>/${PYPI_USER}/" \
        -e "s/<PYPI_PASS>/${PYPI_PASS}/" \
        < "${DIRNAME}/.pypirc.template" > "${HOME}/.pypirc"
    python setup.py register
    python setup.py sdist bdist_wheel
    twine upload -u "${PYPI_USER}" -p "${PYPI_PASS}" dist/*

fi
