from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import models
import schemas # Import your schemas
from database import engine, get_db
from typing import List

# Create tables if they don't exist
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Store Management System",
    description="RESTful Store Management API built with FastAPI, SQLAlchemy, SQLite and Docker.",
    version="1.0.0"
)

@app.get("/")
def home():
    return {"status": "Online", "database": "SQLite (Local File)", "message": "Schemas are ready!"}


@app.post("/employees/", response_model=schemas.EmployeeSchema)
def create_employee(employee: schemas.EmployeeCreateSchema, db: Session = Depends(get_db)):
    db_employee = models.Employee(**employee.dict()) # Create model instance from schema
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    return db_employee # Return the created employee using the output schema

@app.get("/employees/", response_model=List[schemas.EmployeeSchema])
def read_employees(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.Employee).offset(skip).limit(limit).all()

@app.get("/employees/{employee_id}", response_model=schemas.EmployeeSchema)
def read_employee(employee_id: int, db: Session = Depends(get_db)):
    db_employee = db.query(models.Employee).filter(models.Employee.EmployeeID == employee_id).first()
    if db_employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    return db_employee

# --- Product Endpoints ---
@app.post("/products/", response_model=schemas.ProductSchema)
def create_product(product: schemas.ProductCreateSchema, db: Session = Depends(get_db)):
    db_product = models.Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

@app.get("/products/", response_model=List[schemas.ProductSchema])
def read_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.Product).offset(skip).limit(limit).all()

@app.get("/products/{product_id}", response_model=schemas.ProductSchema)
def read_product(product_id: int, db: Session = Depends(get_db)):
    db_product = db.query(models.Product).filter(models.Product.ProductID == product_id).first()
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product

# --- Sale Endpoints (Example with nested details) ---
@app.post("/sales/", response_model=schemas.SaleSchema)
def create_sale(sale: schemas.SaleCreateSchema, db: Session = Depends(get_db)):
    db_sale = models.Sale(
        SaleDate=sale.SaleDate,
        EmployeeID=sale.EmployeeID,
        PaymentMethodID=sale.PaymentMethodID,
        TotalAmount=sale.TotalAmount
    )
    db.add(db_sale)
    db.commit() # Commit sale first to get SaleID
    db.refresh(db_sale) # Refresh to get the generated SaleID

    for detail_data in sale.details:
        # Check if product exists
        product = db.query(models.Product).filter(models.Product.ProductID == detail_data.ProductID).first()
        if not product:
            # Optional: Rollback if a detail product is not found
            # db.rollback()
            raise HTTPException(status_code=404, detail=f"Product with ID {detail_data.ProductID} not found")

        db_sale_detail = models.SaleDetail(
            SaleID=db_sale.SaleID,
            ProductID=detail_data.ProductID,
            Quantity=detail_data.Quantity,
            UnitPrice=detail_data.UnitPrice
        )
        db.add(db_sale_detail)
        # Optional: Update product quantity here if needed
        # product.Quantity -= detail_data.Quantity
        # db.add(product)


    db.commit() # Commit sale details
    db.refresh(db_sale) # Refresh again to potentially get updated related data if needed

    # Optionally fetch details to return with SaleSchema
    sale_details_query = db.query(models.SaleDetail).filter(models.SaleDetail.SaleID == db_sale.SaleID).all()
    # Convert SaleDetail SQLAlchemy objects to SaleDetailSchema
    db_sale.details = [schemas.SaleDetailSchema.from_orm(sd) for sd in sale_details_query]

    return db_sale

@app.get("/sales/", response_model=List[schemas.SaleSchema])
def read_sales(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.Sale).offset(skip).limit(limit).all()

# Add more endpoints for other models as needed...
