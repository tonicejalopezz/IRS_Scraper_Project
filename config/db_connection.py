import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import pandas as pd

def fetch_engine(database_name):
    """
    Datbase connnection in PostgreSQL using SQLAlchemy.
    """
    load_dotenv()
    
    db_user = os.getenv("DB_USER")
    db_password = os.getenv("DB_PASSWORD")
    db_host = os.getenv("DB_HOST")
    db_port = os.getenv("DB_PORT")
    db_name = os.getenv(database_name)

    connection = f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

    try:
    
        engine = create_engine(connection)
        with engine.connect() as con:

            con.execute(text("SELECT 1"))
        print("Database Successfully Connected.")
        return engine

    except Exception as e:

        print("Database Connection Failed.")
        print(f"Error; {e}")
        return None

def main():
    
    db_name = input("Enter the database name: ")
    engine = fetch_engine(db_name)

if __name__ == "__main__":
    main()