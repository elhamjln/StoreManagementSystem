from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# تغییر از PostgreSQL به SQLite برای استفاده محلی و فایل‌محور
# این فایل به نام 'storedb.db' در کنار کدهای شما ساخته می‌شود
DATABASE_URL = "sqlite:///./storedb.db"

# ایجاد انجین (برای SQLite پارامتر check_same_thread الزامی است)
engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

# ایجاد Session برای مدیریت تراکنش‌ها در FastAPI
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# تعریف Base برای مدل‌ها
Base = declarative_base()

# این تابع بسیار مهم است؛ آن را در FastAPI برای دریافت دیتابیس استفاده می‌کنید
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
