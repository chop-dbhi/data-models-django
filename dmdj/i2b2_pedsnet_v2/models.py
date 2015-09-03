import requests
from django.db.models import Model
from dmdj.settings import get_url
from dmdj.makers import make_model

url = get_url('i2b2_pedsnet', 'v2')

model_json = requests.get(url).json()

model = make_model(model_json, (Model,), 'dmdj.i2b2_pedsnet_v2.models',
                   'i2b2_pedsnet_v2')

for table in model:
    globals()[table.__name__] = table
