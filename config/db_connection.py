import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import pandas as pd

class DatabaseConnect:

    def __init__(self, target_db):
        self.target_db = target_db

        load_dotenv()
        self.db_user = os.getenv("DB_USER")
        self.db_password = os.getenv("DB_PASSWORD")
        self.db_host = os.getenv("DB_HOST")
        self.db_port = os.getenv("DB_PORT")
        self.db_name = os.getenv(target_db)
    
    def connect(self):
        """
        Connecting to PostgreSQL databse.
        """
        connection = f"postgresql+psycopg2://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"
        try:
            self.engine = create_engine(connection)
            with self.engine.connect() as con:
                con.execute(text("SELECT 1"))
            print("Database Successfully Connected.")
            return self.engine
        except Exception as e:
            print(f"Database Connection Failed: {e}")

    def get_engine(self):
        """
        Function to consider if an engine is already connected.
        """
        self.engine