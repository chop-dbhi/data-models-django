import requests
from django.db.models import Model
from dmdj.settings import get_url
from dmdj.makers import make_model

url = get_url('i2b2', 'v1.7')

model_json = requests.get(url).json()

model = make_model(model_json, (Model,), 'dmdj.i2b2_v1_7.models',
                   'i2b2_v1_7')

for table in model:
    globals()[table.__name__] = table
