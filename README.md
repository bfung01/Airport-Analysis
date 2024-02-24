# Airflow ETL DAG for Flight Departure Data
This repository contains an Apache Airflow Directed Acyclic Graph (DAG) designed to automate the extraction, transformation, and loading (ETL) of flight departure data from the Airlabs API into an AWS S3 bucket. The workflow is hosted on an Amazon EC2 instance.

## Repository Structure
### /dag: Contains the Airflow DAG file that defines the ETL process.
- DAG File: departures_dag.py
### /analysis: Contains the analysis file 
- Python File: airport_analysis.py
This DAG, named departures_dag, is scheduled to run hourly and is designed to perform the following tasks:

Check Airlabs API Availability: Utilizes an HttpSensor to ensure the Airlabs departure API is reachable before proceeding with data extraction.

Extract Flight Departure Data: A SimpleHttpOperator is used to fetch data from the Airlabs API for a specific airport (JFK in this example). The extraction focuses on fields such as departure and arrival times, flight numbers, delays, and other relevant flight details.

Transform and Load Data: A custom Python function (transform_load_data) transforms the extracted JSON data into a structured format suitable for analytics. It processes each flight's departure time, terminal, airline, and other attributes, then appends the new data to an existing CSV file in an AWS S3 bucket. The process includes deduplication and sorting of the records.

## Setup and Configuration
### Prerequisites
- Apache Airflow 2.0+
- AWS S3 bucket access
- Airlabs API key
## Configuration
1. Airflow Environment: Ensure Airflow is installed and properly configured on your EC2 instance. Refer to the Apache Airflow documentation for installation and setup instructions.
2. AWS S3 Bucket: Ensure you have access to an AWS S3 bucket and that Airflow has the necessary permissions to read from and write to this bucket.
3. Airlabs API Key: Replace the placeholder API key in the DAG file with your actual Airlabs API key.
4. Airflow Connections: Set up the http_conn_id='departure_api' connection in Airflow to point to the Airlabs API endpoint. Ensure the connection includes the base URL and any necessary authentication headers.

## Running the DAG
After configuring the prerequisites and setting up the necessary connections in Airflow, enable the departures_dag DAG in the Airflow UI. The workflow will execute according to its schedule, processing new flight departure data hourly.

## Security
Credentials: Ensure that your Airlabs API key and AWS credentials are securely stored and managed within Airflow. Use Airflow's built-in secrets management to handle sensitive information.
