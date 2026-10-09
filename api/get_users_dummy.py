import requests
from lib.lib import pg_insert_table, get_pg_connection

data = None

try:
    url = 'https://dummyjson.com/users'
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    data = response.json()
    print('Response success')
except requests.RequestException as e:
    raise RuntimeError('Failed to fetch users from API') from e

table = 'users'
users = []
columns = ['user_id', 'first_name', 'last_name', 'age', 'gender', 'email',
            'phone', 'username', 'birth_date', 'address', 'city', 'state']
for elem in data['users']:
    address = elem.get('address') or {}
    user = (elem.get('id'), elem.get('firstName'), elem.get('lastName'), elem.get('age'), elem.get('gender'),
            elem.get('email'),elem.get('phone'), elem.get('username'), elem.get('birthDate'),
            address.get('address'), address.get('city'), address.get('state'))
    users.append(user)

try:
    pg_insert_table(table, columns, users, get_pg_connection())
    print(f'Data {table} inserted successfully')
except Exception as e:
    raise RuntimeError('Failed to insert users into PostgreSQL') from e