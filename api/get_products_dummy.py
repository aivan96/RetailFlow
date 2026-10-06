import requests
from lib.lib import pg_insert_table, get_pg_connection

try:
    url = 'https://dummyjson.com/products'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        print('Response success')
        try:
            table = 'products'
            products = []
            columns = ['product_id', 'title', 'brand', 'category', 'weight', 'return_policy', 'min_order_quantity']
            for elem in data['products']:
                product = (elem.get('id'), elem.get('title'), elem.get('brand'), elem.get('category'),
                           elem.get('weight'), elem.get('returnPolicy'), elem.get('minimumOrderQuantity'))
                products.append(product)

            pg_insert_table(table, columns, products, get_pg_connection())
            print(f'Data {table} inserted successfully')
        except Exception as e:
            print(f'Error inserting data: {e}')
    else:
        print(f'Response failed. Status code: {response.status_code}')
        print(f'Response text: {response.text}')
except Exception as e:
    print(f'Ошибка: {e}')