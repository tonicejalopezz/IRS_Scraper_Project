from config.db_connection import fetch_engine

def main():
    """
    Running ETL process
    """

    ## Fetch Targeted Database Containing Non Profit Organizations
    target_db = "ME_DB" # INPUT COMMAND     
    engine = fetch_engine(target_db)
    
        


    


if __name__ == "__main__":
    main()

