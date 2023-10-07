from airflow import DAG
from datetime import datetime
from airflow.operators.python import PythonOperator
from odds.datamodels import write_objects, dump_objects


with DAG(
    "my-dag",
    start_date=datetime(2023, 10, 6),
    schedule_interval="@daily",
    catchup=False
) as dag:

    dump_data = PythonOperator(
        task_id="dump-data",
        python_callable=write_objects
    )

    write_data = PythonOperator(
        task_id="write-data",
        python_callable=dump_objects
    )

dump_data >> write_data