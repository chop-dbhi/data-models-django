import django
from django.db.models import Model, ForeignKey
from dmdj.makers import make_table

if not django.conf.settings.configured:
    django.conf.settings.configure()

if hasattr(django, 'setup'):
    django.setup()


def test_class_name():

    table_json = {'name': 'test_table', 'fields': [{'type': 'integer',
                                                    'name': 'integer'}]}
    module = 'dmdj.tests'
    app_label = 'dmdj'
    bases = (Model,)
    table = make_table(table_json, {}, [], bases, module,
                       app_label)
    assert table.__name__ == 'TestTable'


def test_module():

    table_json = {'name': 'test_table', 'fields': [{'type': 'integer',
                                                    'name': 'integer'}]}
    module = 'dmdj.tests'
    app_label = 'dmdj'
    bases = (Model,)
    table = make_table(table_json, {}, [], bases, module,
                       app_label)
    assert table.__module__ == 'dmdj.tests'


def test_pk():

    table_json = {'name': 'test_table', 'fields': [{'type': 'integer',
                                                    'name': 'integer'}]}
    constraint_json = {'primary_keys': [{'fields': ['integer']}]}
    module = 'dmdj.tests'
    app_label = 'dmdj'
    bases = (Model,)
    table = make_table(table_json, constraint_json, [], bases, module,
                       app_label)
    assert table._meta.pk.name == 'integer'


def test_no_pk():

    table_json = {'name': 'test_table', 'fields': [{'type': 'integer',
                                                    'name': 'integer'}]}
    module = 'dmdj.tests'
    app_label = 'dmdj'
    bases = (Model,)
    table = make_table(table_json, {}, [], bases, module, app_label)
    assert table._meta.pk.name == 'id'


def test_multi_pk():

    table_json = {'name': 'test_table', 'fields': [{'type': 'integer',
                                                    'name': 'int1'},
                                                   {'type': 'integer',
                                                    'name': 'int2'}]}
    constraint_json = {'primary_keys': [{'fields': ['int1', 'int2']}]}
    module = 'dmdj.tests'
    app_label = 'dmdj'
    bases = (Model,)
    table = make_table(table_json, constraint_json, [], bases, module,
                       app_label)

    assert table._meta.pk.name == 'id'
    assert table._meta.unique_together == (('int1', 'int2'),)

    for field in table._meta.fields:
        if field.name in ['int1', 'int2']:
            assert not field.null


def test_unique():

    table_json = {'name': 'test_table', 'fields': [{'type': 'integer',
                                                    'name': 'integer'}]}
    constraint_json = {'uniques': [{'fields': ['integer']}]}
    module = 'dmdj.tests'
    app_label = 'dmdj'
    bases = (Model,)
    table = make_table(table_json, constraint_json, [], bases, module,
                       app_label)

    for field in table._meta.fields:
        if field.name == 'integer':
            assert field.unique


def test_not_null():

    table_json = {'name': 'test_table', 'fields': [{'type': 'integer',
                                                    'name': 'integer'}]}
    constraint_json = {'not_null': [{'fields': ['integer']}]}
    module = 'dmdj.tests'
    app_label = 'dmdj'
    bases = (Model,)
    table = make_table(table_json, constraint_json, [], bases, module,
                       app_label)

    for field in table._meta.fields:
        if field.name == 'integer':
            assert not field.null


def test_index():

    table_json = {'name': 'test_table', 'fields': [{'type': 'integer',
                                                    'name': 'integer'}]}
    index_json = [{'fields': ['integer']}]
    module = 'dmdj.tests'
    app_label = 'dmdj'
    bases = (Model,)
    table = make_table(table_json, {}, index_json, bases, module,
                       app_label)

    for field in table._meta.fields:
        if field.name == 'integer':
            assert field.db_index


def test_foreign_key():

    table_json = {'name': 'test_table', 'fields': [{'type': 'integer',
                                                    'name': 'integer'}]}
    constraint_json = {'foreign_keys': [{'source_table': 'test_table',
                                         'source_field': 'integer',
                                         'target_table': 'other',
                                         'target_field': 'field'}]}
    module = 'dmdj.tests'
    app_label = 'dmdj'
    bases = (Model,)
    table = make_table(table_json, constraint_json, [], bases, module,
                       app_label)

    for field in table._meta.fields:
        if field.name == 'integer':
            assert isinstance(field, ForeignKey)
            assert field.to_fields[0] == 'field'
            assert field.related_query_name() == 'test_table_integer_set'
