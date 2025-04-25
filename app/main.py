# app/main.py
from fastapi import FastAPI
from .routers import auth

app = FastAPI()

# Include the auth router (register and login routes)
app.include_router(auth.router, tags=["Auth"])

@app.get("/")
def read_root():
    return {"message": "Invoice Generator API is running"}
