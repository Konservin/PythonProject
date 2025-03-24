# app/main.py

from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, Ervin"}

@app.get("/hello")
def greet(name: str = "world"):
    return {"message": f"Hello, {name}!"}
