# models.py
from sqlalchemy import Column, Integer, String, ForeignKey, Numeric, DateTime
from database import Base
from datetime import datetime # Import datetime

# Employee
class Employee(Base):
    __tablename__ = "employees"
    EmployeeID = Column(Integer, primary_key=True, index=True)
    FullName = Column(String(100), nullable=False)
    Phone = Column(String(20), nullable=False)
    EmployeeType = Column(String(20), nullable=False)

# Product
class Product(Base):
    __tablename__ = "products"
    ProductID = Column(Integer, primary_key=True, index=True)
    ProductName = Column(String(100), nullable=False)
    Quantity = Column(Integer, nullable=False, default=0)

# Inventory
class Inventory(Base):
    __tablename__ = "inventory"
    InventoryID = Column(Integer, primary_key=True, autoincrement=True) # Added primary key
    ProductID = Column(Integer, ForeignKey("products.ProductID"))
    Quantity = Column(Integer, nullable=False)

# Payment Method
class PaymentMethod(Base):
    __tablename__ = "payment_methods"
    PaymentMethodID = Column(Integer, primary_key=True, index=True)
    MethodName = Column(String(30), nullable=False)

# Sale
class Sale(Base):
    __tablename__ = "sales"
    SaleID = Column(Integer, primary_key=True, index=True)
    SaleDate = Column(DateTime, default=datetime.utcnow) # Use datetime.utcnow for default
    EmployeeID = Column(Integer, ForeignKey("employees.EmployeeID"))
    PaymentMethodID = Column(Integer, ForeignKey("payment_methods.PaymentMethodID"))
    TotalAmount = Column(Numeric(10, 2))

# Sale Detail
class SaleDetail(Base):
    __tablename__ = "sale_details"
    SaleDetailID = Column(Integer, primary_key=True)
    SaleID = Column(Integer, ForeignKey("sales.SaleID"))
    ProductID = Column(Integer, ForeignKey("products.ProductID"))
    Quantity = Column(Integer)
    UnitPrice = Column(Numeric(10, 2))

# Verification
class Verification(Base):
    __tablename__ = "verifications"
    VerificationID = Column(Integer, primary_key=True)
    SaleID = Column(Integer, ForeignKey("sales.SaleID"))
    VerificationType = Column(String(20))
    ReferenceNumber = Column(String(50))
    VerificationResult = Column(String(20))

# Inventory Report
class InventoryReport(Base):
    __tablename__ = "inventory_reports"
    ReportID = Column(Integer, primary_key=True)
    ReportDate = Column(DateTime, default=datetime.utcnow) # Use datetime.utcnow for default
    EmployeeID = Column(Integer, ForeignKey("employees.EmployeeID"))

# Inventory Report Detail
class InventoryReportDetail(Base):
    __tablename__ = "inventory_report_details"
    ReportDetailID = Column(Integer, primary_key=True)
    ReportID = Column(Integer, ForeignKey("inventory_reports.ReportID"))
    ProductID = Column(Integer, ForeignKey("products.ProductID"))
    Quantity = Column(Integer)
