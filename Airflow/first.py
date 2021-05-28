from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago
import time

def first_execute(*op_args, **op_kwargs):
    print(op_args)
    print(op_kwargs)
    secs = op_args[0]
    secs = secs + op_kwargs['s']
    time.sleep(secs)
    return secs

def second_execute():
    time.sleep(2)
    return 2

with DAG (
    dag_id="first",
    schedule_interval=None, #'*/1 * * * *', #..every 1 minute
    default_args={
        'owner': 'airflow',
        'retries': 1,
        'start_date': days_ago(2),
    }, ) as f:

    first_execute=PythonOperator(
        task_id="first_execute",
        python_callable=first_execute,
        op_args = [5, 5],
        op_kwargs={'s': 1,})