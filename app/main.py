from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app.models import Filter
from app.db import SessionLocal

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/filters")
def list_filters(db: Session = Depends(get_db)):
    filters = db.query(Filter).all()
    return [{"id": f.id, "name": f.name} for f in filters]
