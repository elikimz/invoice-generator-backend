# app/core/config.py
import os

SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key")  # Replace with your actual secret key
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60))