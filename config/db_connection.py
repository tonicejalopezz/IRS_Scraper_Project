import os
from sqlalchemy import create_engine
from dotenv import load_dotenv

def fetch_engine(database_name):

    load_dotenv()
    
    db_user = os.getenv("DB_USER")
    db_password = os.getenv("DB_PASSWORD")
    db_host = os.getenv("DB_HOST")
    db_port = os.getenv("DB_PORT")
    db_name = os.getenv(database_name)

    connection = f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    
    engine = create_engine(connection)
    
    return engine

def main():
    
    db_name = input("Enter the database name: ")
    engine = fetch_engine(db_name)
    print("Database engine created successfully.")

if __name__ == "__main__":
    main()