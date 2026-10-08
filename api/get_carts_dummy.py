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
            columns = ['cart_id', 'user_id', 'total', 'discounted_total', 'total_products', 'total_quantity']
            for elem in data['carts']:
                cart = (elem.get('id'), elem.get('userId'), elem.get('total'), elem.get('discountedTotal'),
                        elem.get('totalProducts'), elem.get('totalQuantity'))
                carts.append(cart)
            pg_insert_table(table, columns, carts, get_pg_connection())
            print(f'Data {table} inserted successfully')
        except Exception as e:
            print(f'Error inserting data: {e}')

        try:
            table = 'cart_items'
            items = []
            columns = ['cart_id', 'product_id', 'title', 'price', 'quantity', 'total', 'discount_percentage',
                       'discounted_total']
            for elem in data['carts']:
                for e in elem['products']:
                    item = (elem.get('id'), e.get('id'), e.get('title'), e.get('price'), e.get('quantity'),
                            e.get('total'), e.get('discountPercentage'), e.get('discountedTotal'))
                    items.append(item)
            pg_insert_table(table, columns, items, get_pg_connection())
            print(f'Data {table} inserted successfully')
        except Exception as e:
            print(f'Error inserting data: {e}')
    else:
        print(f'Response failed. Status code: {response.status_code}')
        print(f'Response text: {response.text}')
except Exception as e:
    print(f'Error: {e}')