import requests
from lib.lib import pg_insert_table, get_pg_connection

data = None

try:
    url = 'https://dummyjson.com/products'
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    data = response.json()
    print('Response success')
except requests.RequestException as e:
    raise RuntimeError('Failed to fetch products from API') from e

table = 'products'
products = []
columns = ['product_id', 'title', 'brand', 'category', 'weight', 'return_policy', 'min_order_quantity']
for elem in data['products']:
    product = (elem.get('id'), elem.get('title'), elem.get('brand'), elem.get('category'),
                elem.get('weight'), elem.get('returnPolicy'), elem.get('minimumOrderQuantity'))
    products.append(product)

try:
    pg_insert_table(table, columns, products, get_pg_connection())
    print(f'Data {table} inserted successfully')
except Exception as e:
    raise RuntimeError('Failed to insert products into PostgreSQL') from e