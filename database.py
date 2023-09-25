from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os
import mysql.connector
from fastapi import HTTPException

load_dotenv()

#if the database is not availavle in database then create it automatically

connection = mysql.connector.connect(
    host=os.getenv("host"),
    port=os.getenv("port"),
    user=os.getenv("user"),
    password=os.getenv("database_password"),
)

# Create a new database (if it doesn't exist)
database_name=os.getenv("database_name")
create_database_query = f"CREATE DATABASE IF NOT EXISTS {database_name}"

cursor = connection.cursor()
try:
    cursor.execute(create_database_query)
    connection.commit()  # Commit the transaction
except mysql.connector.Error as err:
    print(f"Error: {err}")
finally:
    cursor.close()
    connection.close()


#if the database is availabe
url=os.getenv("db_url")

if url is None:
    raise HTTPException("DataBase url is not store .env file")

SQLALCHEMY_DATABASE_URL = url

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, pool_size=200, max_overflow=0
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal() 
    try:
        yield db
    finally:
        db.close()

