# app/models/products.py
from sqlalchemy import Column, BigInteger, String, ForeignKey
from app.db import Base

class SkincareProducts(Base):
    __tablename__ = "skincare_products"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    identifier = Column(String(255), nullable=False, unique=True)
    brand = Column(String(255), nullable=True)
    name = Column(String(255), nullable=True)
    type = Column(String(50), nullable=False)  # e.g., 'serum', 'cleanser'

class SkincareIngredients(Base):
    __tablename__ = "skincare_ingredients"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    product_id = Column(ForeignKey("skincare_products.id", ondelete="CASCADE"), nullable=False)
    ingredient = Column(String(255), nullable=False)
