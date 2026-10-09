from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator

from api import get_carts_dummy, get_products_dummy, get_users_dummy
from pg_to_minio import bronze_carts, bronze_cart_items, bronze_products, bronze_users
from bronze_to_silver import silver_cart_items, silver_products, silver_users, silver_carts
from silver_to_gold import gold_carts_cart_items
from gold_to_ch import ch_carts_cart_items

default_args = {
    'depends_on_past': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    'start_date': datetime(2026, 6, 10),
}

with (DAG(
    dag_id='retailflow',
    default_args=default_args,
    description='Запуск Python-скриптов сервиса RetailFlow',
    schedule='20 18 * * *',
    catchup=False,
) as dag):

    extract_carts_task = PythonOperator(
        task_id='extract_carts_task',
        python_callable=get_carts_dummy
    )

    extract_users_task = PythonOperator(
        task_id='extract_users_task',
        python_callable=get_users_dummy
    )

    extract_products_task = PythonOperator(
        task_id='extract_products_task',
        python_callable=get_products_dummy
    )

    bronze_carts_task = PythonOperator(
        task_id='bronze_carts_task',
        python_callable=bronze_carts
    )

    bronze_cart_items_task = PythonOperator(
        task_id='bronze_cart_items_task',
        python_callable=bronze_cart_items
    )

    bronze_products_task = PythonOperator(
        task_id='bronze_products_task',
        python_callable=bronze_products
    )

    bronze_users_task = PythonOperator(
        task_id='bronze_users_task',
        python_callable=bronze_users
    )

    silver_cart_items_task = PythonOperator(
        task_id='silver_cart_items_task',
        python_callable=silver_cart_items
    )

    silver_products_task = PythonOperator(
        task_id='silver_products_task',
        python_callable=silver_products
    )

    silver_users_task = PythonOperator(
        task_id='silver_users_task',
        python_callable=silver_users
    )

    silver_carts_task = PythonOperator(
        task_id='silver_carts_task',
        python_callable=silver_cart_items
    )

    gold_cart_items_task = PythonOperator(
        task_id='gold_cart_items_task',
        python_callable=gold_carts_cart_items
    )

    ch_cart_items_task = PythonOperator(
        task_id='ch_cart_items_task',
        python_callable=ch_carts_cart_items
    )

    extract_tasks = [extract_carts_task, extract_users_task, extract_products_task]
    bronze_tasks = [bronze_carts_task, bronze_users_task, bronze_products_task, bronze_cart_items_task]
    silver_tasks = [silver_carts_task, silver_users_task, silver_products_task, silver_cart_items_task]

    extract_tasks >> bronze_tasks
    bronze_tasks >> silver_tasks
    silver_tasks >> gold_cart_items_task
    gold_cart_items_task >> ch_cart_items_task