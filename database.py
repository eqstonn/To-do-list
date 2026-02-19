from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()
SQL_DATABASE_URL = os.getenv("DATABASE_URL")

"""
1. Create engine to connect to database via url as parameter
2. Create sesion maker to converse (open & close) with database
3. Create declarative_base, which converts class to sql table
"""

engine = create_engine(SQL_DATABASE_URL)
LocalSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


