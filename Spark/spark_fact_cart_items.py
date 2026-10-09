from pyspark.sql import SparkSession
from minio import Minio
from datetime import datetime
from minio import S3Error
from config.config import conf_spark, conf_minio
import pandas as pd
import io

client = Minio(
    conf_minio['endpoint'],
    access_key=conf_minio['access_key'],
    secret_key=conf_minio['secret_key'],
    secure=False,
    region=conf_minio['region'],
)

bucket_name = 'retailflow'
spark = conf_spark
dt = datetime.now()
df = None

try:
    #cart_items_name = f'silver/cart_items/{dt.year}/{dt.month}/{dt.day}/cart_items.parquet'
    #carts_name = f'silver/carts/{dt.year}/{dt.month}/{dt.day}/carts.parquet'
    cart_items_name = 'silver/cart_items/2026/10/8/cart_items.parquet'
    carts_name = 'silver/carts/2026/10/8/carts.parquet'

    carts_response = client.get_object(bucket_name, carts_name)
    cart_items_response = client.get_object(bucket_name, cart_items_name)

    data_cart_items = cart_items_response.read()
    data_cart = carts_response.read()

    cart_items_df = pd.read_parquet(io.BytesIO(data_cart_items))
    carts_df = pd.read_parquet(io.BytesIO(data_cart))

    carts_spark_df = spark.createDataFrame(carts_df)
    cart_items_spark_df = spark.createDataFrame(cart_items_df)

    df = carts_spark_df.join(cart_items_spark_df, 'cart_id').select('cart_id', 'user_id', 'quantity', 'price')

    print('Tables joined successfully.')
except S3Error as e:
    raise RuntimeError('Error Minio/Spark') from e

try:
    df = df.toPandas()
    object_name = f'Spark/{dt.strftime("%Y-%m-%d")}.parquet'
    parquet_data = df.to_parquet(engine='pyarrow')

    client.put_object(
        bucket_name,
        object_name,
        io.BytesIO(parquet_data),
        length=len(parquet_data),
        content_type='application/parquet',
    )
    print(f'Object {object_name} uploaded successfully.')
except S3Error as e:
    raise RuntimeError('Error with Minio') from e

spark.stop()

#нужно перенастроить подключение, чтобы сразу извлекать датафрейм в спарк, а не пандас - спарк - пандас