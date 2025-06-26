from fastapi import FastAPI, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path

from .database import SessionLocal, engine
from . import models, schemas, crud

# Create tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="ServeSmart API")

# Allow local dev origins, adjust as needed
origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"] ,
    allow_headers=["*"] ,
)

# We'll mount product_images directory.
static_dir = Path(__file__).resolve().parent / "product_images"
app.mount("/product_images", StaticFiles(directory=str(static_dir)), name="product_images")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ---------------- Seller Endpoints ---------------- #

@app.post("/sellers/register", response_model=schemas.SellerCreate)
async def register_seller(seller: schemas.SellerCreate, db: Session = Depends(get_db)):
    existing = db.query(models.Seller).filter(
        (models.Seller.user_name == seller.user_name) | (models.Seller.e_mail == seller.e_mail) | (models.Seller.identity_no == seller.identity_no)
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Seller with provided credentials already exists")
    created = crud.create_seller(db, seller)
    return created

# ---------------- Product Endpoints ---------------- #

@app.post("/products", response_model=schemas.Product)
async def add_product(
    username: str,
    password: str,
    explanation: str,
    price: float,
    image: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    seller = crud.authenticate_seller(db, username, password)
    if not seller:
        raise HTTPException(status_code=401, detail="Invalid seller credentials")

    image_bytes = await image.read()
    product = crud.create_product(db, seller, explanation, price, image_bytes)
    return product

@app.get("/products")
async def search_products(query: str, db: Session = Depends(get_db)):
    products = crud.search_products(db, query)
    return products

@app.get("/products/{product_id}", response_model=schemas.Product)
async def get_product(product_id: int, db: Session = Depends(get_db)):
    product = crud.get_product_by_id(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

# ---------------- Purchase Endpoints ---------------- #

@app.post("/purchase")
async def purchase_product(purchase: schemas.PurchaseCreate, db: Session = Depends(get_db)):
    product = crud.get_product_by_id(db, purchase.product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    crud.increment_purchase_count(db, product)
    crud.create_purchase(db, purchase)
    return {"message": "Product purchased successfully"}

# ---------------- Seller Dashboard ---------------- #

@app.post("/sellers/products", response_model=schemas.SellerProductsResponse)
async def seller_products(login: schemas.SellerLogin, db: Session = Depends(get_db)):
    seller = crud.authenticate_seller(db, login.user_name, login.password)
    if not seller:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    products, total_sales, total_revenue = crud.get_seller_products(db, seller)
    return {
        "products": products,
        "total_sales": total_sales,
        "total_revenue": total_revenue,
    }

@app.delete("/products/{product_id}")
async def delete_product(product_id: int, username: str, password: str, db: Session = Depends(get_db)):
    seller = crud.authenticate_seller(db, username, password)
    if not seller:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    success = crud.delete_product(db, seller, product_id)
    if not success:
        raise HTTPException(status_code=403, detail="You are not authorized to delete this product")
    return {"message": "Product deleted successfully"} 