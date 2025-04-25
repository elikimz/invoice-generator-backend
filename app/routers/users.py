# from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy.orm import Session
# from fastapi.security import OAuth2PasswordRequestForm
# from app import schemas, models
# from app.database import get_db
# from app.routers.auth import create_user, login_user  # Updated login_user to handle OAuth2PasswordRequestForm

# router = APIRouter()

# @router.post("/register", response_model=schemas.UserInDB)
# def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
#     db_user = create_user(db, user)
#     return db_user

# @router.post("/login")
# def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
#     login_response = login_user(db, form_data)
#     if login_response:
#         return login_response
#     raise HTTPException(status_code=400, detail="Invalid credentials")
