from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from fastapi import FastAPI, APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.models import User
from app.schemas import UserCreate, UserInDB
from app.database import get_db
from app.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES

# Initialize FastAPI app
app = FastAPI()

# Password hash verification
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2PasswordBearer for extracting the token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Helper functions
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    if expires_delta is None:
        expires_delta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)  # Use default expiration time
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def authenticate_user(db: Session, email: str, password: str) -> User:
    user = db.query(User).filter(User.email == email).first()
    if user and verify_password(password, user.hashed_password):
        return user
    return None

def create_user(db: Session, user: UserCreate) -> User:
    db_user = User(
        email=user.email,
        full_name=user.full_name,
        hashed_password=hash_password(user.password)
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def login_user(db: Session, form_data: OAuth2PasswordRequestForm):
    user_in_db = authenticate_user(db, form_data.username, form_data.password)  # Using form_data.username as email
    if user_in_db:
        access_token = create_access_token(data={"sub": user_in_db.email})
        return {"access_token": access_token, "token_type": "bearer"}
    return None

# Define router
router = APIRouter()

# Registration endpoint
@router.post("/register", response_model=UserInDB)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = create_user(db, user)
    return db_user

# Login endpoint
@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    login_response = login_user(db, form_data)
    if login_response:
        return login_response
    raise HTTPException(status_code=400, detail="Invalid credentials")

# Include the auth router
app.include_router(router, prefix="/auth", tags=["auth"])

# Test endpoint to check if the app is running
@app.get("/")
def read_root():
    return {"message": "Authentication API is running"}
