import re
import requests
from bs4 import BeautifulSoup
import pandas as pd

def email_extractor(table, website_col="Website"):

  email_pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
  org_emails = []

  for row in table.itertuples(index=False):

    url = getattr(row, website_col)

    if isinstance(url, str):
      
      url = url.strip()

      if not url.startswith(("http://", "https://")):

        url = "https://" + url

      try:

        page = requests.get(url, timeout=10)
        soup = BeautifulSoup(page.text, "html.parser")    
        emails = re.findall(email_pattern, soup.get_text())


        for a_tag in soup.find_all("a", href=True):
          href = a_tag["href"]
          if href.startswith("mailto:"):
            email = href[7:]  
            if re.match(email_pattern, email):
              emails.append(email)

        if emails:
          org_emails.append(emails[0])
        else:
          org_emails.append(None)
          print(f"No emails found for URL: {url}")

      except requests.exceptions.RequestException as e:
        print(f"Error fetching page for URL {url}: {e}")
        org_emails.append(None)

    else:
      print(f"Invalid URL: {url}")
      org_emails.append(None)
    
  table.loc[:, "Emails"] = org_emails
  return table

def main():

  data = pd.read_csv("data/raw/eo_me_org_scrape.csv")

  email_pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
 
  test1 = requests.get("http://www.THEFABULOUSFIND.ORG")
  soup = BeautifulSoup(test1.text, "html.parser")
  emails = re.findall(email_pattern, soup.get_text())
  print(emails)

if __name__ == "__main__":


  main()



  


