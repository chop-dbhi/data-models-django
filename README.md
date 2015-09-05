# Data Models Django

[![Circle CI](https://circleci.com/gh/chop-dbhi/data-models-django/tree/master.svg?style=svg)](https://circleci.com/gh/chop-dbhi/data-models-django/tree/master) [![Coverage Status](https://coveralls.io/repos/chop-dbhi/data-models-django/badge.svg?branch=master&service=github)](https://coveralls.io/github/chop-dbhi/data-models-django?branch=master)

Django models for [chop-dbhi/data-models-service](https://github.com/chop-dbhi/data-models-service) style JSON endpoints.

## Django Model Usage

In your shell, hopefully within a virtualenv:

```sh
pip install dmdj
```

In python:

```python
from dmdj.omop.v5_0_0.models import Person

print Person._meta.fields
```

These models are dynamically generated at runtime from JSON endpoints provided by chop-dbhi/data-models-service, which reads data stored in chop-dbhi/data-models. Each data model version available on the service is included in a dynamically generated python module. At the time of writing, the following are available. Any added to the service will use the same naming conventions.

- **OMOP V4** at `omop.v4_0_0.models`
- **OMOP V5** at `omop.v5_0_0.models`
- **PEDSnet V1** at `pedsnet.v1_0_0.models`
- **PEDSnet V2** at `pedsnet.v2_0_0.models`
- **i2b2 V1.7** at `i2b2.v1_7_0.models`
- **i2b2 PEDSnet V2** at `i2b2_pedsnet.v2_0_0.models`
- **PCORnet V1** at `pcornet.v1_0_0.models`
- **PCORnet V2** at `pcornet.v2_0_0.models`
- **PCORnet V3** at `pcornet.v3_0_0.models`

### Caveats

- This package is **not** a Django "app" and it cannot be included in your Django project `INSTALLED_APPS`. Neither can any of the dynamically created modules (like `pedsnet.v2_0_0`).
- The models are associated with a fictional Django `app_label` when they are dynamically created, so they will not be included in any Django sql output or migration commands. If you would like to explicitly include the models in your app or project, use code similar to the `version_module_code` code block in the [`dmdj/__init__.py`](dmdj/__init__.py) file to re-generate models with your app's `app_label` at runtime.
- The models are dynamically generated and may change over time, although efforts to improve the semantic versioning and stability practices in the data-models repo are under way.
- No attempt is made to provide migrations for any changes that do occur over time.
