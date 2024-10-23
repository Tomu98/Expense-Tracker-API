from app.db import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship


class User(Base):
    """
    Represents a user in the database.
    """
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(30), nullable=False, unique=True)
    email = Column(String(75), nullable=False, unique=True)
    hashed_password = Column(String(150), nullable=False)

    expenses = relationship("Expense", backref="owner", cascade="all, delete-orphan")
