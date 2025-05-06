#!/bin/bash

mkdir -p \
  airflow/dags \
  airflow/plugins \
  data_ingestion \
  data_transformation \
  data_loading \
  config \
  docker \
  tests

touch \
  airflow/dags/etl_products.py \
  data_ingestion/api_client.py \
  data_transformation/product_cleaning.py \
  data_loading/load_to_postgres.py \
  config/db_connection.py \
  tests/test_transformations.py \
  docker/docker-compose.yml \
  requirements.txt \
  README.md \
  .env

echo "Folder Structure Complete"