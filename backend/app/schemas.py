from pydantic import BaseModel, Field, constr, EmailStr
from typing import Optional, List

class SellerCreate(BaseModel):
    user_name: constr(min_length=3, max_length=50)
    identity_no: constr(regex=r"^\d{11}$")
    IBAN: str
    business_address: str
    e_mail: EmailStr
    password: str

class SellerLogin(BaseModel):
    user_name: str
    password: str

class ProductBase(BaseModel):
    product_name: str
    description: Optional[str] = None
    price: float
    discount: float

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    product_id: int
    seller_id: int
    purchase_count: int
    product_image_path: Optional[str] = None

    class Config:
        orm_mode = True

class PurchaseCreate(BaseModel):
    product_id: int
    identity_no: constr(regex=r"^\d{11}$")
    CVV: constr(regex=r"^\d{3}$")
    card_no: str
    address: str
    e_mail: EmailStr

class SellerProductsResponse(BaseModel):
    products: List[Product]
    total_sales: int
    total_revenue: float 