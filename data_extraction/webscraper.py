from config.db_connection import fetch_engine

from bs4 import BeautifulSoup
import requests

import pandas as pd

from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

  
  
def fetch_db_data(engine, table_name):
  """
  Extracting data from PostgreSQL database using SQLAlchemy.
  """
  try:
  
    query = """
    SELECT EIN, NAME
    FROM eo_me;
    """

    
  

  except:
    print(f"Error fetching data from source: {url}")


def main():

  target_db = "ME_DB"
  engine = create_engine(target_db)





   
if __name__ == "__main__":
  main()

