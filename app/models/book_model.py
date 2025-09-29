from config.database import Base
from sqlalchemy import Column, Integer, String, Float
from datetime import datetime

class BookModel(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    author = Column(String, index=True)
    isbn = Column(String, unique=True, index=True)
    cost_usd = Column(Float)
    selling_price_local = Column(Float)
    stock_quantity = Column(Integer)
    category = Column(String, index=True)
    supplier_country = Column(String, index=True)
    created_at = Column(String, default=datetime.utcnow)
    updated_at = Column(String, default=datetime.utcnow, onupdate=datetime.utcnow)
