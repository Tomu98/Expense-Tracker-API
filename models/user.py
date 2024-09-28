from db import Base
from sqlalchemy import Column, Integer, String

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(30), nullable=False, unique=True)
    email = Column(String(75), nullable=False, unique=True)
    hashed_password = Column(String(150), nullable=False)
