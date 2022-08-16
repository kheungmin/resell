from airflow import DAG
from datetime import datetime

from pandas import json_normalize

from airflow.operators.bash import BashOperator


# URL="https://www.luck-d.com/"

 # mongoDB 접속 정보
# client = pymongo.MongoClient('mongodb://team04:1111@ec2-54-95-8-243.ap-northeast-1.compute.amazonaws.com:27017/')
# db = client.resell

default_args = {
    "start_date": datetime(2022, 7, 26) # 2022년 7월 25일 부터 시작.
}

# DAG 설정
with DAG(
    dag_id = "lucky_draw_pipeline",
    schedule_interval = "* */3 * * * *" ,
    # "*/3 * * * *"
    default_args = default_args,
    tags=["lucky", "draw", "pipeline"],
    catchup = False) as dag:

    

    run_scrapy = BashOperator (
        task_id = 'lucky_test',
        bash_command='cd ~/airflow/dags/resell/lucky_draw_air && source activate base && scrapy crawl lucky_draw_air',
        dag=dag
    )
