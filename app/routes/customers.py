from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Customer

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/")
def create_customer(name: str, email: str, phone: str, db: Session = Depends(get_db)):
    customer = Customer(name=name, email=email, phone=phone)
    db.add(customer)
    db.commit()
    db.refresh(customer)
    return customer


@router.get("/")
def get_customers(db: Session = Depends(get_db)):
    return db.query(Customer).all()