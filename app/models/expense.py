from app.db import Base
from sqlalchemy import Column, Integer, String, DECIMAL, DateTime, ForeignKey


class Expense(Base):
    """
    Represents an expense record in the database.
    """
    __tablename__ = "expenses"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    amount = Column(DECIMAL(10, 2), nullable=False)
    category = Column(String(50), nullable=False)
    description = Column(String(200))
    date = Column(DateTime, nullable=False)
