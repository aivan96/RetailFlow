import requests
from lib.lib import pg_insert_table, get_pg_connection

try:
    url = 'https://dummyjson.com/users'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        print('Response success')
        try:
            table = 'users'
            users = []
            columns = ['first_name', 'last_name', 'age', 'gender', 'email',
                       'phone', 'username', 'birth_date', 'address', 'city', 'state']
            for elem in data['users']:
                address = elem.get('address') or {}
                user = (elem.get('firstName'), elem.get('lastName'), elem.get('age'), elem.get('gender'),
                        elem.get('email'),elem.get('phone'), elem.get('username'), elem.get('birthDate'),
                        address.get('address'), address.get('city'), address.get('state'))
                users.append(user)

            pg_insert_table(table, columns, users, get_pg_connection())
            print('Data inserted successfully')
        except Exception as e:
            print(f'Error inserting data: {e}')
    else:
        print(f'Response failed. Status code: {response.status_code}')
        print(f'Response text: {response.text}')
except Exception as e:
    print(f'Error: {e}')