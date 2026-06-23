# schemas.py
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List

# --- Schemas for reading data (output from API) ---

class EmployeeSchema(BaseModel):
    EmployeeID: int
    FullName: str
    Phone: str
    EmployeeType: str

    class Config:
        orm_mode = True # Allows reading data from SQLAlchemy models


class ProductSchema(BaseModel):
    ProductID: int
    ProductName: str
    Quantity: int

    class Config:
        orm_mode = True


class InventorySchema(BaseModel):
    InventoryID: int
    ProductID: int
    Quantity: int

    class Config:
        orm_mode = True

class PaymentMethodSchema(BaseModel):
    PaymentMethodID: int
    MethodName: str

    class Config:
        orm_mode = True

class SaleDetailSchema(BaseModel):
    SaleDetailID: int
    SaleID: int
    ProductID: int
    Quantity: int
    UnitPrice: float # Use float for numeric types from DB

    class Config:
        orm_mode = True

class SaleSchema(BaseModel):
    SaleID: int
    SaleDate: datetime
    EmployeeID: Optional[int] = None
    PaymentMethodID: Optional[int] = None
    TotalAmount: Optional[float] = None
    # You can also include related details if needed, but it can make schemas complex
    # details: List[SaleDetailSchema] = []

    class Config:
        orm_mode = True

class VerificationSchema(BaseModel):
    VerificationID: int
    SaleID: int
    VerificationType: str
    ReferenceNumber: str
    VerificationResult: str

    class Config:
        orm_mode = True

class InventoryReportSchema(BaseModel):
    ReportID: int
    ReportDate: datetime
    EmployeeID: Optional[int] = None

    class Config:
        orm_mode = True

class InventoryReportDetailSchema(BaseModel):
    ReportDetailID: int
    ReportID: int
    ProductID: int
    Quantity: int

    class Config:
        orm_mode = True


# --- Schemas for creating/updating data (input to API) ---

# When creating an Employee, we don't provide EmployeeID (it's auto-generated)
class EmployeeCreateSchema(BaseModel):
    FullName: str
    Phone: str
    EmployeeType: str

# When creating a Product, we don't provide ProductID
class ProductCreateSchema(BaseModel):
    ProductName: str
    Quantity: int = 0 # Default quantity to 0

# For Inventory, maybe we want to update quantity
class InventoryUpdateSchema(BaseModel):
    Quantity: int

# For Payment Methods, creation
class PaymentMethodCreateSchema(BaseModel):
    MethodName: str

# For Sales, we need details as a list
class SaleDetailCreateSchema(BaseModel):
    ProductID: int
    Quantity: int
    UnitPrice: float

class SaleCreateSchema(BaseModel):
    # SaleID is auto-generated
    SaleDate: Optional[datetime] = Field(default_factory=datetime.utcnow)
    EmployeeID: Optional[int] = None
    PaymentMethodID: Optional[int] = None
    TotalAmount: Optional[float] = None
    details: List[SaleDetailCreateSchema] # List of SaleDetail objects


class VerificationCreateSchema(BaseModel):
    SaleID: int
    VerificationType: str
    ReferenceNumber: str
    VerificationResult: str

class InventoryReportDetailCreateSchema(BaseModel):
    ProductID: int
    Quantity: int

class InventoryReportCreateSchema(BaseModel):
    ReportDate: Optional[datetime] = Field(default_factory=datetime.utcnow)
    EmployeeID: Optional[int] = None
    details: List[InventoryReportDetailCreateSchema] # List of details
