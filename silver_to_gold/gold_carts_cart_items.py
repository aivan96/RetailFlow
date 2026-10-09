import pandas as pd
from datetime import datetime
from minio import Minio
from minio import S3Error
from config.config import conf_minio
import io

client = Minio(conf_minio['endpoint'],
               access_key=conf_minio['access_key'],
               secret_key=conf_minio['secret_key'],
               secure=False,
               region=conf_minio['region'])

dt = datetime.now()
df_all = None

try:
    bucket_name = 'retailflow'
    object_carts = f'silver/carts/{dt.year}/{dt.month}/{dt.day}/carts.parquet'
    object_cart_items = f'silver/cart_items/{dt.year}/{dt.month}/{dt.day}/cart_items.parquet'

    response_cart = client.get_object(bucket_name, object_carts)
    response_cart_items = client.get_object(bucket_name, object_cart_items)

    data_carts_bytes = response_cart.read()
    data_cart_items_bytes = response_cart_items.read()

    df_cart = pd.read_parquet(io.BytesIO(data_carts_bytes))
    df_cart_items = pd.read_parquet(io.BytesIO(data_cart_items_bytes))

    df_all = pd.merge(df_cart[['cart_id', 'user_id']],
                      df_cart_items[['cart_id', 'product_id', 'price', 'quantity', 'total', 'discount_percentage']],
                      on='cart_id')
    df_all['snapshot_date'] = dt.date()
    print('Carts and cart items merged')
except S3Error as e:
    raise RuntimeError('Silver error') from e

try:
    object_name = f'gold/fact_cart_items/{dt.strftime("%Y-%m-%d")}.parquet'
    df_all_bytes = df_all.to_parquet(engine='pyarrow')

    client.put_object(
        bucket_name,
        object_name,
        io.BytesIO(df_all_bytes),
        length=len(df_all_bytes),
        content_type='application/parquet'
    )
    print('Gold cart items successfully uploaded')
except S3Error as e:
    raise RuntimeError('Gold error') from e