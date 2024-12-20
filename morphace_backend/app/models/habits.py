# app/models/habits.py
from sqlalchemy import Column, BigInteger, ForeignKey, DateTime, Integer, Boolean
from sqlalchemy.sql import func
from app.db import Base

class UserHabits(Base):
    __tablename__ = "user_habits"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    timestamp = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    sleep_hours = Column(Integer, nullable=True)
    used_spf = Column(Boolean, nullable=True)

class HabitSkincareProducts(Base):
    __tablename__ = "habit_skincare_products"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_habit_id = Column(ForeignKey("user_habits.id", ondelete="CASCADE"), nullable=False)
    product_id = Column(ForeignKey("skincare_products.id", ondelete="CASCADE"), nullable=False)
