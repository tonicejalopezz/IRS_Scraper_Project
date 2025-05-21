# Modules Within This Project
import os

# Libraries
import pandas as pd
from bs4 import BeautifulSoup
import requests
import xmltodict
from dotenv import load_dotenv

class DatabaseHandler:

  def __init__(self, engine):
    self.engine = engine

  def fetch_table(self, table_name, start_letter, end_letter):
    """
    Extracting data from PostgreSQL database using SQLAlchemy with the intention to select
    non exempt organizations within the letter range from the databse.
    """
    query = f"""
    SELECT ein, name, asset_amt, income_amt, revenue_amt
    FROM {table_name}
    WHERE UPPER(LEFT(name, 1)) BETWEEN UPPER('{start_letter}') AND UPPER('{end_letter}')
    ORDER BY NAME ASC;
    """
    try:
      table = pd.read_sql(query, self.engine)
      return table
    except Exception as e:
      print(f"Error Fetching Table {table_name} from PostgreSQL: {e}")

class Form990Info:

  def __init__(self):
    load_dotenv()
    self.main_url = os.getenv("MAIN_URL")
    self.search_url = os.getenv("ORG_URL")

  def scrape_data(self, org_id="ein", organization="name"):
    """
    Scraping data for each EIN specified if they contain an existing 990 form, 
    providing principal officer name, website to then later scrape contacts, and 
    description to later identify the area of focus for the nonprofit organization.
    """
    try:
      page = requests.get(self.search_url + str(org_id))
      page.raise_for_status()
      soup = BeautifulSoup(page.text, "html.parser")
      files = soup.find_all("section", class_="right-content")
      form990 = [form for form in files if form.find("h5") and form.find("h5").text.strip() == "990"]
      if not form990:
        print(f"No form 990 Found For Organization: {organization}, EIN: {org_id}")
        return [None, None, None]
      
      # Form 990s are XML documents
      tag = form990[0].find("a", href=True, string="XML")
      if not tag:
        print(f"Error Parsing form 990 XML document for Organization:{organization}, EIN: {org_id}")
        return [None, None, None]
      
      tag_response = requests.get(self.main_url + tag["href"])
      tag_response.raise_for_status()

      temp = xmltodict.parse(tag_response.content)
      form_path = temp.get("Return", {}).get("ReturnData", {}).get("IRS990", {})
      return [
                form_path.get("PrincipalOfficerNm", None),
                form_path.get("WebsiteAddressTxt", None),
                form_path.get("ActivityOrMissionDesc", None)
            ]

    except requests.exceptions.RequestException as e:
      print(f"Request Error for Organization Name: {organization}, EIN: {org_id} ----- {e}")
      return [None, None, None]
    

class OrgPipeline:

  def __init__(self, engine, scraper):
    self.db_handler = DatabaseHandler(engine)
    self.scraper = scraper

  def fetch_org_data(self, table, id_column="ein", organization="name"):
    """
    For each row in the requested table, contacts will be collected
    if conditions are met.
    """
    officers, websites, descriptions = [], [], []

    for row in table.itertuples(index=False):

      ein = getattr(row, id_column)
      name = getattr(row, organization)

      officer, website, description = self.scraper.scrape_data(ein, name)
      officers.append(officer)
      websites.append(website)
      descriptions.append(description)

    table.loc[:, "principal_officer"] = officers
    table.loc[:, "website"] = websites
    table.loc[:, "description"] = descriptions

    return table

  def run_extract(self, table_name, start_letter, end_letter, output_path):

    req_table = self.db_handler.fetch_table(table_name, start_letter, end_letter)
    ext_table = self.fetch_org_data(req_table)
    ext_table.to_csv(output_path, index=False)