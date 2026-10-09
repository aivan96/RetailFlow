import pandas as pd
import io
from minio import Minio
from minio.error import S3Error
from datetime import datetime
from lib.lib import get_ch_connection, ch_insert
from config.config import conf_minio, ch

client = Minio(
    conf_minio['endpoint'],
    access_key=conf_minio['access_key'],
    secret_key=conf_minio['secret_key'],
    secure=False,
    region=conf_minio['region']
)
dt = datetime.now()
bucket_name = 'retailflow'
object_name = f'gold/fact_cart_items/{dt.strftime("%Y-%m-%d")}.parquet'

try:
    response = client.get_object(bucket_name, object_name)
    data_bytes = response.read()
    df = pd.read_parquet(io.BytesIO(data_bytes))
    print('Parquet file loaded')

    try:
        df = df.fillna({
            "cart_id": 0,
            "user_id": 0,
            "product_id": 0,
            "price": 0.0,
            "quantity": 0,
            "total": 0.0,
            "discount_percentage": 0.0,
        })
        get_ch_connection().insert_df('carts_cart_items', df, 'default')
        print('Clickhouse data inserted successfully')

    except Exception as e:
        print(f'Clickhouse error: {e}')
except S3Error as e:
    print(f'Gold error: {e}')