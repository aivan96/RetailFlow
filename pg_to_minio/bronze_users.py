from minio import Minio
from minio.error import S3Error
from config.config import conf_minio
from lib.lib import get_pg_connection
import pandas as pd
from datetime import datetime
import io

client = Minio(conf_minio['endpoint'],
               access_key=conf_minio['access_key'],
               secret_key=conf_minio['secret_key'],
               secure=conf_minio['secure'],
               region=conf_minio['region'])

bucket_name = 'retailflow'
source = 'users'
json_bytes = None

try:
    source = 'users'
    query = f'SELECT * FROM {source}'
    df = pd.read_sql_query(query, get_pg_connection())
    json_data = df.to_json(orient='records', force_ascii=False)
    json_bytes = json_data.encode('utf-8')
except Exception as e:
    raise RuntimeError('Error with PostgresSQL') from e

try:
    if not client.bucket_exists(bucket_name):
        client.make_bucket(bucket_name)
        print(f'Bucket {bucket_name} created successfully.')
    dt = datetime.now()
    object_name = f"bronze/{source}/{dt.year}/{dt.month}/{dt.day}/{source}.json"

    client.put_object(
        bucket_name,
        object_name,
        io.BytesIO(json_bytes),
        length=len(json_bytes),
        content_type='application/json'
    )
    print(f'Object {object_name} uploaded successfully.')
except S3Error as e:
    raise RuntimeError('Error while connecting to Minio') from e