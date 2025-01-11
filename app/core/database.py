from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from decouple import config

SQLALCHEMY_DATABASE_URL = config("SQLALCHEMY_DATABASE_URL")

# starting point for the SQL Alchemy application
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# session to interact with db
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# base class for declarative models - create tables by using Python classes
Base = declarative_base()

# instance of session, this can be injected anywhere
def get_db():
    db = SessionLocal()
    try:
        yield db # create a new session for each request, instead of just 1 session for a whole app
    finally:
        db.close()