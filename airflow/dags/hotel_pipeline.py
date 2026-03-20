from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.postgres_operator import PostgresOperator

from datetime import datetime

with DAG(
    dag_id = "hotel_pipeline",
    start_date=datetime(2024,1,1),
    schedule_interval="@daily",
    catchup=False
) as dag:
    init = BashOperator(
        task_id = "init",
        bash_command ='''
        psql "postgresql://${DB_USER}:${DB_PASS}@${DB_HOST}/${DB_NAME}?sslmode=require" -c "
    CREATE SCHEMA IF NOT EXISTS _bronze;
    CREATE SCHEMA IF NOT EXISTS _silver;
    CREATE SCHEMA IF NOT EXISTS _gold;
    CREATE TABLE IF NOT EXISTS _bronze.hotel_prices (
        id SERIAL PRIMARY KEY,
        scrape_date TEXT,
        checkin_date TEXT,
        hotel_name TEXT,
        price TEXT,
        stars TEXT,
        dist_to_haram TEXT,
        link TEXT);
    CREATE TABLE IF NOT EXISTS _silver.hotel_prices (
        id TEXT,
        scrape_date DATE,
        checkin_date DATE,
        hotel_name TEXT,
        price NUMERIC,
        stars INT,
        dist_to_haram NUMERIC,
        link TEXT);
    CREATE TABLE IF NOT EXISTS _bronze.scrape_logs (
        id SERIAL PRIMARY KEY,
        run_time TEXT,
        status TEXT,
        rows_inserted TEXT,
        error_message TEXT);
        "
    '''
    )

    scrape = BashOperator(
        task_id = "run_scraper",
        bash_command = "python /opt/umrah_hotels_pipeline/main.py"
    )
    create_silver = BashOperator(
        task_id = "dbt_create_silver",
        bash_command = "cd /opt/umrah_hotels_pipeline/dbt && dbt run --select create_silver --profiles-dir ."
    )
    create_gold = BashOperator(
        task_id = "dbt_create_gold",
        bash_command = "cd /opt/umrah_hotels_pipeline/dbt && dbt run --select gold --profiles-dir ."
    )
init >> scrape >> create_silver >> create_gold

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2026, 3, 17),
}


