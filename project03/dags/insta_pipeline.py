from datetime import datetime

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

from resell.insta_celeb_monitoring import slack


default_args = {
    "start_date": datetime(2022, 7, 26)
}


with DAG(
    dag_id='insta_alert_service',
    schedule_interval='@daily',
    default_args=default_args,
    tags=['insta', 'alert', 'slack'],
    catchup=False) as dag:

    insta_monitor = BashOperator(
        task_id='insta_monitor',
        bash_command='cd ~/airflow/dags/resell/insta_celeb_monitoring/ && source activate base && python insta_monitor.py',
        dag=dag
    )

    model_predict = BashOperator(
        task_id='model_predict',
        bash_command='cd ~/airflow/dags/resell/insta_celeb_monitoring/ && source activate base && python insta_model_prediction.py',
        dag=dag
    )

    slack_alert = PythonOperator(
        task_id='slack_alert',
        python_callable=slack.send_slack,
        dag=dag
    )

    insta_monitor >> model_predict >> slack_alert