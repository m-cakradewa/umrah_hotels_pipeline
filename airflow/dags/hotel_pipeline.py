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
    create_silver = BashOperator(
        task_id = "dbt_create_silver",
        bash_command = "cd /opt/umrah_hotels_pipeline/dbt && dbt run --select create_silver --profiles-dir ."
    )
scrape >> create_silver
#     run_dbt = BashOperator(
#         task_id = "run_dbt_models",
#         bash_command = "cd opt/umrah_hotels_pipeline/dbt_project && dbt run"
#     )

# scrape >> run_dbt