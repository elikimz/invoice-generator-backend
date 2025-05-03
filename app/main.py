
from fastapi import FastAPI
from .routers import auth

app = FastAPI()


app.include_router(auth.router, tags=["Auth"])

@app.get("/")
def read_root():
    return {"message": "Invoice Generator API is    running"}