from sqlalchemy.orm import Session
from typing import List, Optional

from . import models, schemas, utils

# Seller operations

def create_seller(db: Session, seller: schemas.SellerCreate) -> models.Seller:
    db_seller = models.Seller(**seller.dict())
    db.add(db_seller)
    db.commit()
    db.refresh(db_seller)
    return db_seller

def authenticate_seller(db: Session, username: str, password: str) -> Optional[models.Seller]:
    return db.query(models.Seller).filter(models.Seller.user_name == username, models.Seller.password == password).first()

# Product operations

def create_product(db: Session, seller: models.Seller, exp: str, price: float, image_bytes: bytes) -> models.Product:
    discount = utils.calculate_discount()
    title, description = utils.generate_title_description(exp)

    final_price = price - discount
    image_filename = f"{title.replace(' ', '')}.jpg"
    image_path = utils.save_image_from_upload(image_bytes, image_filename)

    db_product = models.Product(
        seller_id=seller.seller_id,
        product_name=title,
        description=description,
        price=final_price,
        product_image_path=image_path,
        discount=discount,
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def search_products(db: Session, query: str) -> List[models.Product]:
    return db.query(models.Product).filter(models.Product.product_name.ilike(f"%{query}%")).all()

def get_product_by_id(db: Session, product_id: int) -> Optional[models.Product]:
    return db.query(models.Product).filter(models.Product.product_id == product_id).first()

def increment_purchase_count(db: Session, product: models.Product):
    product.purchase_count += 1
    db.commit()

# Customer operations

def create_purchase(db: Session, purchase: schemas.PurchaseCreate):
    db_customer = models.Customer(
        identity_no=purchase.identity_no,
        CVV=purchase.CVV,
        card_no=purchase.card_no,
        address=purchase.address,
        e_mail=purchase.e_mail,
    )
    db.add(db_customer)
    db.commit()

# Seller product summary

def get_seller_products(db: Session, seller: models.Seller):
    products = db.query(models.Product).filter(models.Product.seller_id == seller.seller_id).all()
    total_sales = sum(p.purchase_count for p in products)
    total_revenue = sum(p.price * p.purchase_count for p in products)
    return products, total_sales, total_revenue

def delete_product(db: Session, seller: models.Seller, product_id: int) -> bool:
    product = db.query(models.Product).filter(models.Product.product_id == product_id).first()
    if product and product.seller_id == seller.seller_id:
        db.delete(product)
        db.commit()
        return True
    return False 