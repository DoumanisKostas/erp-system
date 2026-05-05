from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Product

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/")
def create_product(name: str, price: float, stock: int, db: Session = Depends(get_db)):
    product = Product(name=name, price=price, stock=stock)
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


@router.get("/")
def get_products(db: Session = Depends(get_db)):
    return db.query(Product).all()

@router.delete("/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()

    if not product:
        return {"error": "Product not found"}

    db.delete(product)
    db.commit()

    return {
        "message": "Product deleted",
        "product_id": product_id
    }

@router.put("/{product_id}")
def update_product(
    product_id: int,
    name: str,
    price: float,
    stock: int,
    db: Session = Depends(get_db)
):
    product = db.query(Product).filter(Product.id == product_id).first()

    if not product:
        return {"error": "Product not found"}

    product.name = name
    product.price = price
    product.stock = stock

    db.commit()
    db.refresh(product)

    return product