from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Filter(Base):
    __tablename__ = "filters"

    id = Column(Integer, primary_key=True)
    name = Column(String)

