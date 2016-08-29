from dmdj.makers import make_meta


def test_db_table():

    table_json = {'name': 'test'}
    meta = make_meta(table_json, {}, [], '')
    assert meta.db_table == 'test'


def test_app_label():

    table_json = {'name': 'test'}
    app_label = 'test'
    meta = make_meta(table_json, {}, [], app_label)
    assert meta.app_label == 'test'


def test_indexes():

    table_json = {'name': 'test'}
    index_json = [{'fields': ['foo', 'bar']}]
    meta = make_meta(table_json, {}, index_json, '')
    assert meta.index_together == [['foo', 'bar']]


def test_uniques():

    table_json = {'name': 'test'}
    constraint_json = {'uniques': [{'fields': ['foo', 'bar']}]}
    meta = make_meta(table_json, constraint_json, [], '')
    assert meta.unique_together == (('foo', 'bar'),)
