import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

load_dotenv()


# PostgreSQL database connection URL
URL = os.getenv("URL")


# Create the connection engine
engine = create_engine(URL)


# Configuring local session
sessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


# Declarative base for models
Base = declarative_base()
