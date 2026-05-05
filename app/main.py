from fastapi import FastAPI
from app.database import engine, Base
from app.routes import products, customers, sales, reports
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

app.include_router(products.router, prefix="/products", tags=["Products"])
app.include_router(customers.router, prefix="/customers", tags=["Customers"])
app.include_router(sales.router, prefix="/sales", tags=["Sales"])
app.include_router(reports.router, prefix="/reports", tags=["Reports"])


@app.get("/", tags=["System"])
def home():
    return {"message": "ERP API is running 🚀"}