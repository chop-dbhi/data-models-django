import django
from django.db.models import Model, ForeignKey
from dmdj.makers import make_model

if not django.conf.settings.configured:
    django.conf.settings.configure()

if hasattr(django, 'setup'):
    django.setup()

model_json = {
    'schema': {
        'constraints': {
            'foreign_keys': [{'source_table': 'test_table_1',
                              'source_field': 'integer',
                              'target_table': 'test_table_2',
                              'target_field': 'integer'}],
            'not_null': [{'table': 'test_table_1', 'field': 'string'}],
            'uniques': [{'table': 'test_table_2', 'fields': ['integer']}],
            'primary_keys': [{'table': 'test_table_1', 'fields': ['pk']}]
        },
        'indexes': [{'table': 'test_table_2', 'fields': ['string']}]
    },
    'tables': [{'name': 'test_table_1', 'fields': [{'type': 'integer',
                                                    'name': 'pk'},
                                                   {'type': 'integer',
                                                    'name': 'integer'},
                                                   {'type': 'string',
                                                    'name': 'string',
                                                    'length': 0}]},
               {'name': 'test_table_2', 'fields': [{'type': 'integer',
                                                    'name': 'integer'},
                                                   {'type': 'string',
                                                    'name': 'string',
                                                    'length': 0}]}]
}


def test_pk():

    module = 'dmdj.tests'
    app_label = 'dmdj'
    bases = (Model,)
    model = make_model(model_json, bases, module, app_label)

    for table in model:
        if table.__name__ == 'TestTable1':
            assert table._meta.pk.name == 'pk'


def test_unique():

    module = 'dmdj.tests'
    app_label = 'dmdj'
    bases = (Model,)
    model = make_model(model_json, bases, module, app_label)

    for table in model:
        if table.__name__ == 'TestTable2':
            for field in table._meta.fields:
                if field.name == 'integer':
                    assert field.unique


def test_not_null():

    module = 'dmdj.tests'
    app_label = 'dmdj'
    bases = (Model,)
    model = make_model(model_json, bases, module, app_label)

    for table in model:
        if table.__name__ == 'TestTable1':
            for field in table._meta.fields:
                if field.name == 'string':
                    assert not field.null


def test_index():

    module = 'dmdj.tests'
    app_label = 'dmdj'
    bases = (Model,)
    model = make_model(model_json, bases, module, app_label)

    for table in model:
        if table.__name__ == 'TestTable2':
            for field in table._meta.fields:
                if field.name == 'string':
                    assert field.db_index


def test_foreign_key():

    module = 'dmdj.tests'
    app_label = 'dmdj'
    bases = (Model,)
    model = make_model(model_json, bases, module, app_label)

    for table in model:
        if table.__name__ == 'TestTable1':
            for field in table._meta.fields:
                if field.name == 'integer':
                    assert isinstance(field, ForeignKey)
                    assert field.to_fields[0] == 'integer'
                    assert field.related_query_name() == \
                        'test_table_1_integer_set'
