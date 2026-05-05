from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import SessionLocal
from app.models import Product, SaleItem

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ========================
# TOTAL REVENUE
# ========================

@router.get("/total-revenue")
def total_revenue(db: Session = Depends(get_db)):
    total = db.query(func.sum(SaleItem.price)).scalar()
    return {"total_revenue": total if total else 0}


# ========================
# LOW STOCK
# ========================

@router.get("/low-stock")
def low_stock(limit: int = 5, db: Session = Depends(get_db)):
    products = db.query(Product).filter(Product.stock <= limit).all()

    return {
        "limit": limit,
        "low_stock_products": products
    }


# ========================
# TOP PRODUCTS
# ========================

@router.get("/top-products")
def top_products(db: Session = Depends(get_db)):
    results = (
        db.query(
            Product.id,
            Product.name,
            func.sum(SaleItem.quantity),
            func.sum(SaleItem.price)
        )
        .join(SaleItem, Product.id == SaleItem.product_id)
        .group_by(Product.id, Product.name)
        .order_by(func.sum(SaleItem.quantity).desc())
        .all()
    )

    return [
        {
            "product_id": row[0],
            "product_name": row[1],
            "total_quantity_sold": row[2],
            "total_revenue": row[3]
        }
        for row in results
    ]