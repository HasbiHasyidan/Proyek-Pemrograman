from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import pandas as pd

# Fungsi untuk membaca data
def extract_data(**kwargs):
    df = pd.read_csv('data/transactions.csv')
    kwargs['ti'].xcom_push(key='raw_data', value=df.to_dict())

# Fungsi untuk transformasi data
def transform_data(**kwargs):
    raw_data = kwargs['ti'].xcom_pull(key='raw_data', task_ids='extract')
    df = pd.DataFrame(raw_data)
    df['Tanggal'] = pd.to_datetime(df['Tanggal'])
    df['Saldo Kumulatif'] = (df['Uang Masuk'] - df['Uang Keluar']).cumsum()
    df.to_csv('data/processed_data.csv', index=False)

# Definisi DAG
default_args = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}
with DAG(
    dag_id='finance_pipeline',
    default_args=default_args,
    description='Pipeline Data Keuangan Harian',
    schedule_interval='@daily',
    start_date=datetime(2024, 12, 1),
    catchup=False,
) as dag:
    task_extract = PythonOperator(
        task_id='extract',
        python_callable=extract_data,
    )

    task_transform = PythonOperator(
        task_id='transform',
        python_callable=transform_data,
    )

    task_extract >> task_transform
