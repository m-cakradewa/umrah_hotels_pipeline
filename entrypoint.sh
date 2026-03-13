#!/bin/bash
# Init DB if not exists
airflow db migrate

airflow users create \
--username "$AIRFLOW_USERNAME" \
--firstname admin \
--lastname admin \
--role Admin \
--email admin@example.com \
--password "$AIRFLOW_PASSWORD" || true

# Start scheduler in background
airflow scheduler &

# Start webserver
exec airflow webserver --port 8080