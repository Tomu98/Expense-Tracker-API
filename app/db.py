import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


# Load environment variables
load_dotenv()


# PostgreSQL database connection URL
URL = os.getenv("DATABASE_URL")

# Ensure the URL is available
if not URL:
    raise ValueError("Database URL is missing. Please set the 'URL' environment variable.")


# Create the connection engine
engine = create_engine(URL)


# Configuring local session
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


# Declarative base for models
Base = declarative_base()
