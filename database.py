import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

# .env dosyasını yükle (eğer varsa, lokal geliştirme için)
load_dotenv()

# Veritabanı bağlantı URL'sini önce ortam değişkenlerinden (Jenkins için),
# sonra .env dosyasından (lokal için) al.
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("Veritabanı bağlantısı için DATABASE_URL ortam değişkeni ayarlanmalıdır.")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """
    Veritabanı tablolarını (eğer mevcut değilse) oluşturur.
    """
    Base.metadata.create_all(bind=engine)
