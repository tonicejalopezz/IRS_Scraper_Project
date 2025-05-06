from bs4 import BeautifulSoup
import requests

import pandas as pd

from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

def organizations_id(data):
  try:
    org_csv = pd.read_csv(data).dropna()

  except:
    print(f"Error Reading CSV File: {data}")
  

def fetch_nonprofit_info(url):
  """
  Fetches the HTML content of a given URL.
  """
  try:
    
    page = requests.get(url)
    print(page.text)

  except:
    print(f"Error fetching data from source: {url}")


def main():

  load_dotenv()

  url = os.getenv("ORG_URL")
  fetch_nonprofit_info(url)

  
  



if __name__ == "__main__":
  main()

