import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pandas as pd
import os 
from config.db_connection import fetch_engine

def reference_uploader(path, database_name):
  """
  Uploading the reference data to the database. This CSV file could only be manually uploaded.
  The reference contains non profit organizations id's from the targeted states database in PostgreSQL.
  """
  engine = fetch_engine(database_name)
  data = pd.read_csv(path)

  filename = os.path.basename(path).split(".")[0]

  data.to_sql(filename, engine, if_exists='replace', index=False)
  print(f"Data from {filename} uploaded to {database_name} database.")

def main():

  target_db = input("Target Datbase: ")
  path = input("Path to the Reference Data: ")

  reference_uploader(path, target_db)

if __name__ == "__main__":

  main()
