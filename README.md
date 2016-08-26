# Data Models Django

[![Circle CI](https://circleci.com/gh/chop-dbhi/data-models-django/tree/master.svg?style=svg)](https://circleci.com/gh/chop-dbhi/data-models-django/tree/master) [![Coverage Status](https://coveralls.io/repos/chop-dbhi/data-models-django/badge.svg?branch=master&service=github)](https://coveralls.io/github/chop-dbhi/data-models-django?branch=master)

Django model generator for [chop-dbhi/data-models-service](https://data-model-service.research.chop.edu) style JSON metadata.

## Installation

If you're not using a Python virtual environment, please do. I prefer [pyenv](https://github.com/yyuu/pyenv) with [pyenv-virtualenv](https://github.com/yyuu/pyenv-virtualenv).

Get the most recent stable version:

```
pip install dmdj
```

Or build and install the (unstable) `HEAD` version:

```
git clone https://github.com/chop-dbhi/data-models-django.git
cd data-models-django
make install
```

## Usage

Place the following in your app's `models.py` file:

```python
import requests
from django.db import models
from dmdj.settings import get_url
from dmdj.makers import make_model

model_url = get_url('pednet', '2.1.0')
model_json = requests.get(model_url).json()

for model in make_model(model_json, (models.Model,), module='yourapp.models',
                        app_label='yourapp')
    globals()[model.__name__] = model
```

This code causes a single web request at runtime, which may slow down your app's startup. Also, the models are dynamically generated and so may change over time, although efforts to improve the semantic versioning and stability practices in the data-models repo are under way.

## Development

### Installation

Install the development requirements and the package in "editable" mode.

```
git clone https://github.com/chop-dbhi/data-models-django.git
cd data-models-django
make devinstall
```

### Testing

Tests are run on the source code using `tox` to replicate them across the range of compatible `Django` and `Python` versions, for the `Python` versions you have available in your environment. I like to create a `dmdj` virtual environment from `3.5.x` and then use `pyenv local dmdj 3.4.x 2.7.x`

```
make test
```

### Coverage

Generate test coverage information that prints in the terminal and creates HTML and XML format files.

```
make coverage
```

## Deployment

These tasks are routinely handled by the CI/CD workflow, but I'll document them here anyway.

### Coveralls

Publish test coverage information to coveralls (the project must be registered and the token must be in the `COVERALLS_REPO_TOKEN` env var).

```
make coveralls
```

### Release

Release a new final version by pushing a new tag to GitHub and uploading the dist files to PyPi (the project must be registered at PyPi and you must have PyPi credentials available or in the `PYPI_USER` and `PYPI_PASS` env vars).

```
make release
```
