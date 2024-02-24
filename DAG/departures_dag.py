from airflow import DAG
from datetime import timedelta, datetime
from airflow.providers.http.sensors.http import HttpSensor
import json
from airflow.providers.http.operators.http import SimpleHttpOperator
from airflow.operators.python import PythonOperator
import pandas as pd
from datetime import datetime
import calendar

def transform_load_data(task_instance):
    data = task_instance.xcom_pull(task_ids="extract_departure_data")
    departures = data['response']
    rows = []
    for flight in departures:
        datetime_object = datetime.strptime(flight['dep_time'], '%Y-%m-%d %H:%M')
        year = flight['dep_time'].split()[0].split('-')[0]
        month = flight['dep_time'].split()[0].split('-')[1]
        day = flight['dep_time'].split()[0].split('-')[2]
        day_of_week = calendar.day_name[datetime_object.weekday()]
        departure_airport = flight['dep_iata']
        terminal = flight['dep_terminal']
        airline = flight['airline_iata']
        flight_num = flight['flight_iata']
        departure_time = flight['dep_time'].split()[1]
        departure_hour = datetime_object.hour
        departure_minute = datetime_object.minute
        delay = flight['dep_delayed']
        arrival_airport = flight['arr_iata']
        if('arr_time' in flight):
            arrival_time = flight['arr_time'].split()[1]
        else:
            arrival_time = None
        duration = flight['duration']

        transformed_data = {"Year": year,
                            "Month": month,
                            "Day": day,
                            "Day of Week": day_of_week,
                            "Departure": departure_airport,
                            "Terminal": terminal,
                            "Airline": airline,
                            "Flight Number": flight_num,
                            "Departure Time": departure_time,
                            "Departure Hour": departure_hour,
                            "Departure Minute": departure_minute,
                            "Delay": delay,
                            "Arrival": arrival_airport,
                            "Arrival Time": arrival_time,
                            "Duration": duration
                            }
        rows.append(transformed_data)
    new_data = pd.DataFrame(rows)
    existing_data = pd.read_csv("BUCKET_PATH")

    complement = pd.concat([existing_data, new_data], ignore_index=True)
    complement.drop_duplicates(inplace=True, keep=False)
    complement.dropna(inplace=True)
    complement.sort_values(by=['Year', 'Month', 'Day', 'Departure Time'], ascending = [True, True, True, True], inplace = True)
    complement.to_csv("BUCKET_PATH", index=False)



default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email': [],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 2,
    'retry_delay': timedelta(minutes=2)
}



with DAG('departures_dag',
        default_args = default_args,
        schedule_interval = '@hourly',
        catchup=False) as dag:
            
            
        is_departure_api_ready = HttpSensor(
        task_id ='is_departure_api_ready',
        http_conn_id='departure_api',
        endpoint='/api/v9/schedules/?api_key=YOUR_API_KEY&dep_iata=JFK&_fields=dep_iata,dep_terminal,airline_iata,flight_iata,dep_time,dep_delayed,arr_iata,arr_time,duration'
    )

        extract_departure_data = SimpleHttpOperator(
        task_id = 'extract_departure_data',
        http_conn_id = 'departure_api',
        endpoint='/api/v9/schedules/?api_key=YOUR_API_KEY&dep_iata=JFK&_fields=dep_iata,dep_terminal,airline_iata,flight_iata,dep_time,dep_delayed,arr_iata,arr_time,duration',
        method = 'GET',
        response_filter= lambda x: json.loads(x.text),
        log_response=True
    )

        transform_load_departure_data = PythonOperator(
        task_id= 'transform_load_departure_data',
        python_callable=transform_load_data
    )




is_departure_api_ready >> extract_departure_data >> transform_load_departure_data
