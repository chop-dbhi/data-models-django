import os
import requests

URL_TEMPLATE = os.environ.get('URL_TEMPLATE') or \
    'http://data-models.origins.link/schemata/{model}/{version}?format=json'

MODELS_URL = os.environ.get('MODELS_URL') or \
    'http://data-models.origins.link/models?format=json'

models_request = requests.get(MODELS_URL)

models_json = models_request.json()

DMS_VERSION = models_request.headers['User-Agent'].split(' ')[0].split('/')[1]

MODELS = []

for model in models_json:

    for model_store in MODELS:

        if model_store['name'] == model['name']:

            model_store['versions'].append({
                'name': model['version'],
                'url': URL_TEMPLATE.format(model=model['name'],
                                           version=model['version'])
            })

            break
    else:

        MODELS.append({
            'name': model['name'],
            'versions': [
                {
                    'name': model['version'],
                    'url': URL_TEMPLATE.format(model=model['name'],
                                               version=model['version'])
                }
            ]
        })


def get_url(model, version):

    for m in MODELS:
        if m['name'] == model:
            for v in m['versions']:
                if v['name'] == version:
                    return v['url']
