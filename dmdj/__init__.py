import os

serial = os.environ.get('BUILD_NUM') or '0'
sha = os.environ.get('COMMIT_SHA1') or '0'
if sha:
    sha = sha[0:8]

__version_info__ = {
    'major': 0,
    'minor': 3,
    'micro': 7,
    'releaselevel': 'final',
    'serial': serial,
    'sha': sha
}


def get_version(short=False):
    assert __version_info__['releaselevel'] in ('alpha', 'beta', 'final')
    vers = ['%(major)i.%(minor)i.%(micro)i' % __version_info__, ]
    if __version_info__['releaselevel'] != 'final' and not short:
        __version_info__['lvlchar'] = __version_info__['releaselevel'][0]
        vers.append('%(lvlchar)s%(serial)s+%(sha)s' % __version_info__)
    return ''.join(vers)

__version__ = get_version()

import sys
import imp
from dmdj.settings import MODELS

version_module_code = """
import requests
from django.db.models import Model
from dmdj.settings import get_url
from dmdj.makers import make_model

url = get_url('{name}', '{version}')

model_json = requests.get(url).json()

model = make_model(model_json, (Model,), 'dmdj.{name}.{version}',
                   'dmdj_{name}_{version}')

for table in model:
    globals()[table.__name__] = table
"""

for model in MODELS:

    path = 'dmdj.' + model['name']
    module = imp.new_module(path)
    module.__file__ = '(dynamically constructed)'
    module.__dict__['__package__'] = 'dmdj'
    locals()[model['name']] = module
    sys.modules[path] = module

    for version in model['versions']:

        version_name = 'v' + version['name'].replace('.', '_')
        version_path = path + '.' + version_name
        version_module = imp.new_module(version_path)
        version_module.__file__ = '(dynamically constructed)'
        version_module.__dict__['__package__'] = 'dmdj'
        setattr(module, version_name, version_module)
        sys.modules[version_path] = version_module

        models_path = version_path + '.models'
        models_module = imp.new_module(models_path)
        models_module.__file__ = '(dynamically constructed)'
        models_module.__dict__['__package__'] = 'dmdj'
        setattr(version_module, 'models', models_module)

        code = version_module_code.format(name=model['name'],
                                          version=version['name'])

        exec(code, models_module.__dict__)
        sys.modules[models_path] = models_module
