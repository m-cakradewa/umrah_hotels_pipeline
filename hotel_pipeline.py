from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

with DAG(
    dag_id = "hotel_pipeline",
    start_date=datetime(2024,1,1),
    schedule_interval="@daily",
    catchup=False
) as dag:
    scrape = BashOperator(
        task_id = "run_scraper",
        bash_command = "python /opt/umrah_hotels_pipeline/main.py"
    )