import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config.db_connection import fetch_engine

from bs4 import BeautifulSoup
import requests
import xmltodict

import pandas as pd

from dotenv import load_dotenv
import os

def fetch_table(engine, table_name, start_letter, end_letter):
  """
  Extracting data from PostgreSQL database using SQLAlchemy.
  """

  query = f"""
  SELECT ein, name, asset_amt, income_amt, revenue_amt
  FROM {table_name}

  WHERE UPPER(LEFT(name, 1)) BETWEEN UPPER('{start_letter}') AND UPPER('{end_letter}')

  ORDER BY NAME ASC;
  """

  try:

    table = pd.read_sql(query, engine)
    return table
  
  except Exception as e:
    print(f"Error fetching table {table_name}: {e}")
    return None
  
def scrape_data(org_id):
  """
  Scraping data for each EIN from target URL.
  """

  load_dotenv()

  search_url = os.getenv("ORG_URL")
  main_url = os.getenv("MAIN_URL")

  try:

    page = requests.get(search_url + str(org_id))

    soup = BeautifulSoup(page.text, "html.parser")

    filings = soup.find_all("section", class_="right-content")
    form990s = [filing for filing in filings if filing.find("h5") and filing.find("h5").text.strip() == "990"]

    if len(form990s) >= 1:
      
      tag = form990s[0].find("a", href=True, string="XML")

      if tag:
        try: 

          tag_response = requests.get(main_url + tag["href"])
          tag_response.raise_for_status()

          temp = xmltodict.parse(tag_response.content)

          form_path = temp.get("Return", {}).get("ReturnData", {}).get("IRS990", {})
          org_officer = form_path.get("PrincipalOfficerNm", None)
          website = form_path.get("WebsiteAddressTxt", None)
          description = form_path.get("ActivityOrMissionDesc", None)

          return [org_officer, website, description]
        
        except requests.exceptions.RequestException as e:
          print(f"Error fetching XML data for EIN {org_id}: {e}")
          return [None, None, None]
        
      else:
        print(f"Error parsing XML data for EIN {org_id}")
        return [None, None, None]
        
    else:
      print(f"No 990 form found for EIN {org_id}")
      return [None, None, None]
    
  except requests.exceptions.RequestException as e:
    print(f"Error fetching page for EIN {org_id}: {e}")
    return [None, None, None]
  
def fetch_org_data(table, id_column="ein"):

  officer_list = []
  website_list = []
  description_list = []

  for row in table.itertuples(index=False):

    ein = getattr(row, id_column)

    officer, website, description = scrape_data(ein)

    officer_list.append(officer)
    website_list.append(website)
    description_list.append(description)

  table.loc[:, "Principal_Officer"] = officer_list
  table.loc[:, "Website"] = website_list
  table.loc[:, "Description"] = description_list

  return table

def main():

  target_db = "ME_DB"
  engine = fetch_engine(target_db)
  table = fetch_table(engine, table_name="eo_me", start_letter="A", end_letter="K")

  test_table = table.iloc[0:50, :]
  
  test_table = fetch_org_data(test_table)

  output = os.path.join("data/raw", "eo_me_org_scrape.csv")
  test_table.to_csv(output, index=False)

if __name__ == "__main__":
  main()

