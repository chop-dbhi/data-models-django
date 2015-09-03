import requests
from django.db.models import Model
from dmdj.settings import get_url
from dmdj.makers import make_model

url = get_url('pcornet', 'v1')

model_json = requests.get(url).json()

model = make_model(model_json, (Model,), 'dmdj.pcornet_v1.models',
                   'pcornet_v1')

for table in model:
    globals()[table.__name__] = table
