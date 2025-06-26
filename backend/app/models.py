from sqlalchemy import Column, Integer, String, Float, ForeignKey, Text
from sqlalchemy.orm import relationship

from .database import Base

class Seller(Base):
    __tablename__ = "sellers"

    seller_id = Column(Integer, primary_key=True, index=True)
    user_name = Column(String(50), unique=True, nullable=False)
    identity_no = Column(String(11), unique=True, nullable=False)
    IBAN = Column(String(34), nullable=False)
    business_address = Column(String, nullable=False)
    e_mail = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)

    products = relationship("Product", back_populates="seller", cascade="all, delete-orphan")

class Product(Base):
    __tablename__ = "products"

    product_id = Column(Integer, primary_key=True, index=True)
    seller_id = Column(Integer, ForeignKey("sellers.seller_id"))
    product_name = Column(String, nullable=False)
    description = Column(Text)
    purchase_count = Column(Integer, default=0)
    product_image_path = Column(String)
    price = Column(Float, nullable=False)
    discount = Column(Float, nullable=False)

    seller = relationship("Seller", back_populates="products")

class Customer(Base):
    __tablename__ = "customers"

    customer_id = Column(Integer, primary_key=True, index=True)
    identity_no = Column(String(11), nullable=False)
    CVV = Column(String(3), nullable=False)
    card_no = Column(String, nullable=False)
    address = Column(String, nullable=False)
    e_mail = Column(String, nullable=False) 