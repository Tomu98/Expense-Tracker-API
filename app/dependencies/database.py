from fastapi import Depends
from sqlalchemy.orm import Session
from app.db import SessionLocal
from typing import Annotated


def get_db():
    """
    Provides a database session to use in API requests. It yields a session and ensures
    it is properly closed after the request is processed.

    Yields:
        Session: SQLAlchemy session for interacting with the database.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
