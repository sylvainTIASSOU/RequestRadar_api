from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

import os


load_dotenv()


SQLALCHEMY_DATABASE_URL="postgresql://default:Yq5hfFJN0mEK@ep-shiny-cell-91515215.us-east-1.aws.neon.tech:5432/verceldb?sslmode=require"
#os.getenv("SQLALCHEMY_DATABASE_URL")


engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()