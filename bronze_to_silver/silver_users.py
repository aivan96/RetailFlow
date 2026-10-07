import pandas as pd
import io
from minio import Minio
from minio.error import S3Error
from config.config import conf_minio

print(conf_minio)

client = Minio()