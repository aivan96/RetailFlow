import pandas as pd
import io
from datetime import datetime
from minio import Minio
from minio.error import S3Error
from config.config import conf_minio

client = Minio(
    conf_minio['endpoint'],
    access_key=conf_minio['access_key'],
    secret_key=conf_minio['secret_key'],
    secure=False,
    region=conf_minio['region']
)

dt = datetime.now()
source = 'products'
bucket_name = 'retailflow'
response = None
silver_df = None

try:
    object_name = f'bronze/{source}/{dt.year}/{dt.month}/{dt.day}/{source}.json'
    response = client.get_object(bucket_name, object_name)
    data_bytes = response.read()
    df = pd.read_json(io.BytesIO(data_bytes))
    print('Data successfully read')

    silver_df = df[['product_id', 'title', 'weight', 'return_policy', 'min_order_quantity',
                    'created_at']].copy()
    batch_id = int(dt.strftime('%Y%m%d%H%M%S'))
    silver_df['converted_at'] = dt
    silver_df['batch_id'] = batch_id
    print('Data successfully converted')

    try:
        object_name = f'silver/{source}/{dt.year}/{dt.month}/{dt.day}/{source}.parquet'
        parquet_data = silver_df.to_parquet(engine='pyarrow')

        client.put_object(
            bucket_name,
            object_name,
            io.BytesIO(parquet_data),
            length=len(parquet_data),
            content_type='application/parquet',
        )
        print(f'Silver data successfully uploaded')
    except S3Error as e:
        print(f'Silver error: {e}')

except S3Error as e:
    print(f'Bronze error: {e}')