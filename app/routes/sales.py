from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Product, Sale, Customer, SaleItem
from typing import List
from pydantic import BaseModel

router = APIRouter()



class SaleItemCreate(BaseModel):
    product_id: int
    quantity: int


class MultiSaleRequest(BaseModel):
    customer_id: int
    items: List[SaleItemCreate]



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@router.post("/")
def create_sale(customer_id: int, db: Session = Depends(get_db)):
    customer = db.query(Customer).filter(Customer.id == customer_id).first()

    if not customer:
        return {"error": "Customer not found"}

    sale = Sale(customer_id=customer_id)

    db.add(sale)
    db.commit()
    db.refresh(sale)

    return {
        "message": "Sale created",
        "sale_id": sale.id,
        "customer_id": customer.id
    }



@router.get("/")
def get_sales(db: Session = Depends(get_db)):
    return db.query(Sale).all()



@router.post("/multi")
def create_sale_multi(request: MultiSaleRequest, db: Session = Depends(get_db)):
    customer = db.query(Customer).filter(Customer.id == request.customer_id).first()

    if not customer:
        return {"error": "Customer not found"}

    sale = Sale(customer_id=request.customer_id)
    db.add(sale)
    db.commit()
    db.refresh(sale)

    total_price = 0
    sold_items = []

    for item in request.items:
        product = db.query(Product).filter(Product.id == item.product_id).first()

        if not product:
            return {"error": f"Product {item.product_id} not found"}

        if product.stock < item.quantity:
            return {"error": f"Not enough stock for {product.name}"}

        item_total = product.price * item.quantity
        product.stock -= item.quantity

        sale_item = SaleItem(
            sale_id=sale.id,
            product_id=product.id,
            quantity=item.quantity,
            price=item_total
        )

        db.add(sale_item)

        total_price += item_total

        sold_items.append({
            "product_id": product.id,
            "product_name": product.name,
            "quantity": item.quantity,
            "item_total": item_total,
            "remaining_stock": product.stock
        })

    db.commit()

    return {
        "message": "Multi sale completed",
        "sale_id": sale.id,
        "customer_id": customer.id,
        "customer_name": customer.name,
        "total_price": total_price,
        "items": sold_items
    }



@router.get("/{sale_id}")
def get_sale_details(sale_id: int, db: Session = Depends(get_db)):
    sale = db.query(Sale).filter(Sale.id == sale_id).first()

    if not sale:
        return {"error": "Sale not found"}

    customer = db.query(Customer).filter(Customer.id == sale.customer_id).first()
    items = db.query(SaleItem).filter(SaleItem.sale_id == sale.id).all()

    result_items = []
    total_price = 0

    for item in items:
        product = db.query(Product).filter(Product.id == item.product_id).first()

        result_items.append({
            "product_id": product.id,
            "product_name": product.name,
            "quantity": item.quantity,
            "price": item.price
        })

        total_price += item.price

    return {
        "sale_id": sale.id,
        "customer": customer.name,
        "items": result_items,
        "total_price": total_price
    }