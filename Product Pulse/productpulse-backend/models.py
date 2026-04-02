from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import declarative_base, relationship
import datetime

Base = declarative_base()

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    category = Column(String, index=True)
    price = Column(Float)
    stock = Column(Integer)
    
    reviews = relationship("Review", back_populates="product")
    competitor_prices = relationship("CompetitorPrice", back_populates="product")

class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    text = Column(String)
    sentiment_score = Column(Float)
    
    product = relationship("Product", back_populates="reviews")

class CompetitorPrice(Base):
    __tablename__ = "competitor_prices"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    competitor_name = Column(String)
    competitor_price = Column(Float)
    checked_at = Column(DateTime, default=datetime.datetime.utcnow)

    product = relationship("Product", back_populates="competitor_prices")