from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import pymysql
from dotenv import load_dotenv
import os

load_dotenv()



DB_URL_WITHOUT_DB = os.getenv("DB_URL_WITHOUT_DB")
DATABASE_NAME = os.getenv("DATABASE_NAME")

DATABASE_URL = f"{DB_URL_WITHOUT_DB}{DATABASE_NAME}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def create_database():
    try: 
        engine_without_db = create_engine(DB_URL_WITHOUT_DB)
        connection = engine_without_db.connect()
        connection.execute(text(f"CREATE DATABASE IF NOT EXISTS {DATABASE_NAME}"))
        connection.close()
        print("Database created successfully")
    except pymysql.MySQLError as e:
        print(f"Error creating database: {e}")
        raise
    


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
