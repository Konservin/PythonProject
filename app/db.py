from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "mysql+pymysql://youruser:yourpass@localhost:3306/yourdbname"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
