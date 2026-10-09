import requests
from lib.lib import pg_insert_table, get_pg_connection

data = None

try:
    url = 'https://dummyjson.com/carts'
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    data = response.json()
    print('Response success')
except requests.RequestException as e:
    raise RuntimeError('Failed to fetch carts from API') from e

table = 'carts'
carts = []
columns = ['cart_id', 'user_id', 'total', 'discounted_total', 'total_products', 'total_quantity']
for elem in data['carts']:
    cart = (elem.get('id'), elem.get('userId'), elem.get('total'), elem.get('discountedTotal'),
            elem.get('totalProducts'), elem.get('totalQuantity'))
    carts.append(cart)

try:
    pg_insert_table(table, columns, carts, get_pg_connection())
    print(f'Data {table} inserted successfully')
except Exception as e:
    raise RuntimeError('Failed to insert carts into PostgreSQL') from e