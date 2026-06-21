from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DATABASE_URL = "mysql+pymysql://root:root@localhost/clothes_ecommerce"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()


# DB session dependency 
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
