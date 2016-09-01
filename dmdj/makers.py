from copy import copy
from django.db.models import (IntegerField, DecimalField, CharField, DateField,
                              DateTimeField, ForeignKey, TextField, FloatField,
                              TimeField, BooleanField, BinaryField)

FIELD_TYPE_MAP = {
    'integer': IntegerField,
    'number': DecimalField,
    'decimal': DecimalField,
    'float': FloatField,
    'string': CharField,
    'date': DateField,
    'datetime': DateTimeField,
    'timestamp': DateTimeField,
    'time': TimeField,
    'text': TextField,
    'clob': TextField,
    'boolean': BooleanField,
    'blob': BinaryField
}

FIELD_KWARGS_MAP = {
    'default': 'default',
    'description': 'help_text',
    'label': 'verbose_name',
    'name': 'db_column'
}

PKEY_JSON = {
    'default': '',
    'description': 'Auto-generated primary key for Django compatability.',
    'label': '',
    'length': 0,
    'name': 'id',
    'precision': 0,
    'required': False,
    'scale': 0,
    'table': '',
    'type': 'integer'
}


def make_field(field_json, constraints, indexes):
    """Returns a dynamically constructed Django model Field class.

    `field_json` is a declarative style nested field object retrieved from the
    chop-dbhi/data-models service or at least matching the format specified
    there.

    `constraints` is a dictionary of constraint lists retrieved from the
    chop-dbhi/data-models service or matching that format. Only relevant
    constraints should be included.

    `indexes` is a list of index objects retrieved from chop-dbhi/data-models
    or similar. Only relevant indexes should be included.
    """

    args = []
    kwargs = {}

    datatype = FIELD_TYPE_MAP[field_json['type']]

    for k, v in field_json.items():
        if v and k in FIELD_KWARGS_MAP:
            kwargs[FIELD_KWARGS_MAP[k]] = v

    if datatype == CharField:
        kwargs['max_length'] = field_json['length'] or 255

    if datatype == DecimalField:
        kwargs['max_digits'] = field_json['precision'] or 20
        kwargs['decimal_places'] = field_json['scale'] or 10

    if constraints.get('primary_keys') and \
            len(constraints['primary_keys'][0]['fields']) == 1:
        kwargs['primary_key'] = True
        kwargs.pop('max_digits', None)
        kwargs.pop('decimal_places', None)

    if constraints.get('uniques') and \
            len(constraints['uniques'][0]['fields']) == 1:
        kwargs['unique'] = True

    for index in indexes:
        if len(index['fields']) == 1:
            kwargs['db_index'] = True

    kwargs['null'] = 'not_null' not in constraints

    if constraints.get('foreign_keys'):

        datatype = ForeignKey
        fkey_json = constraints['foreign_keys'][0]

        target_model_name = ''.join((i.capitalize() for i in
                                     fkey_json['target_table'].split('_')))

        args.append(target_model_name)

        kwargs.pop('max_digits', None)
        kwargs.pop('decimal_places', None)
        kwargs['to_field'] = fkey_json['target_field']
        kwargs['related_name'] = '%s_%s_set' % (fkey_json['source_table'],
                                                fkey_json['source_field'])

    return datatype(*args, **kwargs)


def make_meta(table_json, constraints, indexes, app_label):
    """Returns a dynamically constructed Django model Meta class.

    `table_json` is a declarative style nested table object retrieved from the
    chop-dbhi/data-models service or at least matching the format specified
    there.

    `constraints` is a dictionary of constraint lists retrieved from the
    chop-dbhi/data-models service or matching that format. Only relevant
    constraints should be included.

    `indexes` is a list of index objects retrieved from chop-dbhi/data-models
    or similar. Only relevant indexes should be included.

    `app_label` is the string `app_label`, which will be included in the
    models' Meta classes. It is useful for associating the models with a
    particular Django app.
    """

    class_contents = {'db_table': table_json['name'], 'app_label': app_label}

    multi_idxs = []

    for index in indexes:
        if len(index['fields']) > 1:
            multi_idxs.append(copy(index['fields']))

    class_contents['index_together'] = multi_idxs

    multi_uqs = []

    if 'uniques' in constraints:
        for unique in constraints['uniques']:
            if len(unique['fields']) > 1:
                multi_uqs.append(tuple(unique['fields']))

    class_contents['unique_together'] = tuple(multi_uqs)

    return type(str('Meta'), (), class_contents)


def make_table(table_json, constraints, indexes, bases, module, app_label):
    """Returns a dynamically constructed Django table model class.

    `table_json` is a declarative style nested table object retrieved from the
    chop-dbhi/data-models service or at least matching the format specified
    there.

    `constraints` is a dictionary of constraint lists retrieved from the
    chop-dbhi/data-models service or matching that format. Only relevant
    constraints should be included.

    `indexes` is a list of index objects retrieved from chop-dbhi/data-models
    or similar. Only relevant indexes should be included.

    `bases` is a tuple of base classes the produced model should inherit from.
    This could simply be (django.db.models.Model,).

    `module` is the dot separated string path of the module within which the
    models will reside. It is required by the Django model constructor.

    `app_label` is the string `app_label`, which will be included in the
    models' Meta classes. It is useful for associating the models with a
    particular Django app.
    """

    class_name = ''.join((i.capitalize() for i in
                          table_json['name'].split('_')))

    class_contents = {'__module__': module}

    if constraints.get('primary_keys') and \
            len(constraints['primary_keys'][0]['fields']) > 1:

        if 'uniques' not in constraints:
            constraints['uniques'] = []

        constraints['uniques'].append({
            'name': 'xnk_%s' % table_json['name'],
            'table': table_json['name'],
            'fields': copy(constraints['primary_keys'][0]['fields'])
        })

        if 'not_null' not in constraints:
            constraints['not_null'] = []

        for field in constraints['primary_keys'][0]['fields']:
            constraints['not_null'].append({
                'table': table_json['name'],
                'field': field
            })

    if not constraints.get('primary_keys') or \
            len(constraints['primary_keys'][0]['fields']) > 1:

        pkey_json = copy(PKEY_JSON)
        pkey_json['table'] = table_json['name']
        table_json['fields'].append(pkey_json)

        constraints['primary_keys'] = [{
            'name': 'xpk_%s' % table_json['name'],
            'table': table_json['name'],
            'fields': ['id']
        }]

    class_contents['Meta'] = make_meta(table_json, constraints, indexes,
                                       app_label)

    for field_json in table_json['fields']:

        field_cons = {}

        for con_type, con_list in constraints.items():

            field_cons[con_type] = []

            for con in con_list:

                if 'fields' not in con:
                    fields = [con.get('field') or con.get('source_field')]
                else:
                    fields = con['fields']
                if field_json['name'] in fields:
                    field_cons[con_type].append(con)

        field_idxs = []

        for index in indexes:
            if field_json['name'] in index['fields']:
                field_idxs.append(index)

        class_contents[field_json['name']] = make_field(field_json, field_cons,
                                                        field_idxs)

    return type(str(class_name), bases, class_contents)


def make_model(data_model, bases, module, app_label):
    """Returns a list of dynamically constructed Django model classes.

    `data_model` is a declarative style nested data model object retrieved from
    the chop-dbhi/data-models service or at least matching the format specified
    there.

    `bases` is a tuple of base classes the produced models should inherit from.
    This could simply be (django.db.models.Model,).

    `module` is the dot separated string path of the module within which the
    models will reside. It is required by the Django model constructor.

    `app_label` is the string `app_label`, which will be included in the
    models' Meta classes. It is useful for associating the models with a
    particular Django app.
    """

    output_models = []

    for table_json in data_model['tables']:

        table_cons = {}

        for con_type, con_list in data_model['schema']['constraints'].items():

            table_cons[con_type] = []

            for con in con_list:
                table_name = con.get('table') or con.get('source_table')
                if table_name == table_json['name']:
                    table_cons[con_type].append(con)

        table_idxs = []

        for index in data_model['schema']['indexes']:
            if index['table'] == table_json['name']:
                table_idxs.append(index)

        output_models.append(make_table(table_json, table_cons, table_idxs,
                                        bases, module, app_label))

    return output_models
