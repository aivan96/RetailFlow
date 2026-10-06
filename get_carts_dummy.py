import requests
from lib.lib import pg_insert_table, get_pg_connection

try:
    url = 'https://dummyjson.com/carts'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        print('Response success')
        try:
            table = 'carts'
            carts = []
            columns = ['title', 'price', 'quantity', 'total', 'discount_percentage',
                       'discounted_total', 'customer_id']
            for elem in data['carts']:
                e = elem['products'][1]
                cart = (e.get('title'), e.get('price'), e.get('quantity'), e.get('total'), e.get('discountPercentage'),
                        e.get('discountedTotal'), elem.get('id'))
                carts.append(cart)

            pg_insert_table(table, columns, carts, get_pg_connection())
            print('Data inserted successfully')
        except Exception as e:
            print(f'Error inserting data: {e}')
    else:
        print(f'Response failed. Status code: {response.status_code}')
        print(f'Response text: {response.text}')
except Exception as e:
    print(f'Ошибка: {e}')