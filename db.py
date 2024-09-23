from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

url = ""

engine = create_engine(url)

sessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

base = declarative_base()
