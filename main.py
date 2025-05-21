from config.db_connection import fetch_engine
from data_extraction.webscraper import *
from data_extraction.emailscraper import * 

def main():
    """
    Running ETL process
    """

    # Fetch Targeted Database Containing Non Profit Organizations
    target_db = "ME_DB" # INPUT COMMAND     
    engine = fetch_engine(target_db)

    scraper = Form990Info()
    pipeline = OrgPipeline(engine, scraper)

    output_path = os.path.join("data/raw", "eo_me_org_scrape.csv")

    pipeline.run_extract(table_name="eo_me", start_letter="A", end_letter="K", output_path=output_path)

if __name__ == "__main__":
    main()

