from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# Veritabanı ile iletişim kuran ana motor
engine = create_engine(DATABASE_URL)
# Veritabanı üzerinde işlem yapmamızı (oturum açmamızı) sağlayan yapı
sessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Tablolarımızı miras alacağımız temel sınıf
Base = declarative_base()

# FastAPI'nin her istekte yeni bir DB oturumu açıp kapatması için gereken fonksiyon
def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()
