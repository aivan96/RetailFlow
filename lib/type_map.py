static_type_map = {
    'PG': {
        'CH': {
            'int2': 'Int16',
            'int4': 'Int32',
            'int8': 'Int64',
            'varchar': 'String',
            'timestamp': 'DateTime',
            'timestamptz': 'DateTime',
            'float4': 'Float32',
            'float8': 'Float64',
            'numeric': 'Decimal(12, 2)',
            'date': 'Date',
            'bool': 'Bool',
            'char': 'String',
            'text': 'String',
            'uuid': 'UUID',
            'default': 'String',
        }
    }
}

pg_id_map = {
    22: 'int2',
    23: 'int4',
    20: 'int8',
    1043: 'varchar',
    1114: 'timestamp',
    1184: 'timestamptz',
    700: 'float4',
    701: 'float8',
    1700: 'numeric',
    1082: 'date',
    16: 'bool',
    18: 'char',
    25: 'text',
    2950: 'uuid',
}