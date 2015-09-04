from __future__ import unicode_literals

from nose.tools import ok_, eq_
from django.db.models import (IntegerField, DecimalField, CharField, DateField,
                              DateTimeField, ForeignKey, TextField, FloatField,
                              TimeField, BooleanField, BinaryField)
from dmdj.makers import make_field


def test_types():

    fields_json = [
        {'type': 'integer', 'name': 'integer'},
        {'type': 'number', 'name': 'number', 'precision': 10, 'scale': 5},
        {'type': 'decimal', 'name': 'decimal', 'precision': 10, 'scale': 5},
        {'type': 'float', 'name': 'float'},
        {'type': 'string', 'name': 'string', 'length': 128},
        {'type': 'date', 'name': 'date'},
        {'type': 'datetime', 'name': 'datetime'},
        {'type': 'timestamp', 'name': 'timestamp'},
        {'type': 'time', 'name': 'time'},
        {'type': 'text', 'name': 'text'},
        {'type': 'clob', 'name': 'clob'},
        {'type': 'boolean', 'name': 'boolean'},
        {'type': 'blob', 'name': 'blob'}
    ]

    field_types = [
        IntegerField,
        DecimalField,
        DecimalField,
        FloatField,
        CharField,
        DateField,
        DateTimeField,
        DateTimeField,
        TimeField,
        TextField,
        TextField,
        BooleanField,
        BinaryField
    ]

    for i in range(len(fields_json)):
        field = make_field(fields_json[i], {}, [])
        assert isinstance(field, field_types[i])


def test_char_length():

    field_json = {'type': 'string', 'name': 'string', 'length': 128}
    field = make_field(field_json, {}, [])
    eq_(field.max_length, 128)


def test_char_default_length():

    field_json = {'type': 'string', 'name': 'string', 'length': 0}
    field = make_field(field_json, {}, [])
    eq_(field.max_length, 255)


def test_decimal_precision_scale():

    field_json = {'type': 'decimal', 'name': 'decimal', 'precision': 50,
                  'scale': 15}
    field = make_field(field_json, {}, [])
    eq_(field.max_digits, 50)
    eq_(field.decimal_places, 15)


def test_decimal_precision_scale_defaults():

    field_json = {'type': 'decimal', 'name': 'decimal', 'precision': 0,
                  'scale': 0}
    field = make_field(field_json, {}, [])
    eq_(field.max_digits, 20)
    eq_(field.decimal_places, 10)


def test_primary_key():

    field_json = {'type': 'integer', 'name': 'integer'}
    constraint_json = {'primary_keys': [{'fields': ['integer']}]}
    field = make_field(field_json, constraint_json, [])
    ok_(field.primary_key)


def test_unique():

    field_json = {'type': 'integer', 'name': 'integer'}
    constraint_json = {'uniques': [{'fields': ['integer']}]}
    field = make_field(field_json, constraint_json, [])
    ok_(field.unique)


def test_index():

    field_json = {'type': 'integer', 'name': 'integer'}
    index_json = [{'fields': ['integer']}]
    field = make_field(field_json, {}, index_json)
    ok_(field.db_index)


def test_foreign_key():

    field_json = {'type': 'integer', 'name': 'integer'}
    constraint_json = {'foreign_keys': [{'source_table': 'test',
                                         'source_field': 'integer',
                                         'target_table': 'other',
                                         'target_field': 'field'}]}
    field = make_field(field_json, constraint_json, [])
    assert isinstance(field, ForeignKey)
    eq_(field.to_fields[0], 'field')
    eq_(field.related_query_name(), 'test_integer_set')
