import sys
import json
import requests
import time
import logging
import uuid
from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
from kafka import KafkaProducer



# sys.path.append('./api-request')

api_url = f"https://randomuser.me/api/"

def fetch_data():
    print("Fetching data from randomuser API.....")
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        print(f"API response received successfully")
        res = response.json()
        res = res['results'][0]
        return res
    
    except requests.exceptions.RequestException as e:
        print(f"An error occured: {e}")
        raise

def format_data(res):
    data = {}
    location = res['location']
    # data['id'] = uuid.uuid4()
    data['first_name'] = res['name']['first']
    data['last_name'] = res['name']['last']
    data['gender'] = res['gender']
    data['address'] = f"{str(location['street']['number']) + ', ' + str(location['street']['name'])+ ', '}"\
                        f"{str(location['city']) + ', ' + location['state'] + ', ' + location['country']}"
    data['post_code'] = location['postcode']
    data['email'] = res['email']
    data['username'] = res['login']['username']
    data['dob'] = res['dob']['date']
    data['registered_date'] = res['registered']['date']
    data['phone'] = res['phone']
    data['picture'] = res['picture']['medium']

    return data

def stream_data():

    producer = KafkaProducer(bootstrap_servers=['broker:29092'], max_block_ms=5000)
    curr_time = time.time()
    while True:
        if time.time() > curr_time + 60:
            break
        try:
            res = fetch_data()
            res = format_data(res)
            # print(json.dumps(res, indent=3))
            
            producer.send('user_created', json.dumps(res).encode('utf-8'))

        except Exception as e:
            logging.error(f"An error occured: {e}")
            continue


default_args = {
    'description': 'Kafka Stream DAG',
    'start_date': datetime(2026,1,1),
    'catchup': False
}

dag = DAG(
    dag_id = 'real-time-data-streaming',
    default_args = default_args,
    schedule = '@daily'
    
)

with dag:
    task1 = PythonOperator(
        task_id = 'ingest_data_task',
        python_callable = stream_data
    )

