import clickhouse_connect
import psycopg2
from config.config import ch, pg_prod_fbe

def get_ch_connection():
    return clickhouse_connect.get_client(**ch)

def get_pg_connection():
    return psycopg2.connect(**pg_prod_fbe)

def table_exists(client, db, table):
    query = f"""
        SELECT count()
        FROM system.tables
        WHERE database = '{db}'
        AND name = '{table}'
    """
    result = client.query(query)
    return result.result_rows[0][0] == 1

def ch_struct_to_columns_expr(structure):
    columns = []
    for c in structure:
        columns.append(f'`{c[0]}` {c[1]}')
    return ",\n\t".join(columns)

def ch_create_local(schema, table, structure, connection, partition_by='tuple()', order_by='tuple()'):
    columns_expr = ch_struct_to_columns_expr(structure)
    connection.command(f"""
    CREATE TABLE IF NOT EXISTS {schema}.{table}_local
    ( 
        {columns_expr}
    ) 
    engine = MergeTree() 
    PARTITION BY {partition_by}
    ORDER BY {order_by}
    SETTINGS storage_policy = 'default', index_granularity = 8192
    """)

def ch_create_dist(schema, table, structure, connection, sharding_key='rand()'):
    columns_expr = ch_struct_to_columns_expr(structure)
    connection.command(f"""
    CREATE TABLE IF NOT EXISTS {schema}.{table}
    ( 
        {columns_expr}
    ) 
    engine = Distributed('default', '{schema}', '{table}_local', {sharding_key});
    """)

def ch_insert(schema, table, data, ch_connection):
    sql = f'INSERT INTO {schema}.{table} VALUES {data}'
    ch_connection.command(sql)

def pg_struct_to_columns_expr(structure):
    columns = []
    for c in structure:
        columns.append(f'{c[0]} {c[1]}')
    return ",\n".join(columns)

def pg_create_table(table, structure, conn):
    cursor = conn.cursor()
    columns_expr = pg_struct_to_columns_expr(structure)
    sql = f"""
    CREATE TABLE IF NOT EXISTS {table}
    (
        {columns_expr}
    )
    """
    cursor.execute(sql)
    conn.commit()
    cursor.close()

def pg_insert_table(table, columns, rows, conn):
    cols = ", ".join(f'"{c}"' for c in columns)
    placeholders = ", ".join(["%s"] * len(columns))
    sql = f"""
    INSERT INTO "{table}" ({cols}) 
    VALUES ({placeholders})
    """
    with conn.cursor() as cur:
        cur.executemany(sql, rows)
    conn.commit()
