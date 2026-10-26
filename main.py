import os
from datetime import datetime, timedelta, timezone

import bcrypt
import jwt
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from sqlalchemy import text
from sqlalchemy.orm import Session

from database import engine, Base, SessionLocal
import models

SECRET_KEY = os.getenv("SECRET_KEY", "change-this-secret")
ALGORITHM = "HS256"
ROLES = ["Benefit Owner", "Reviewer", "Finance Manager", "Leadership", "Admin"]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://value-realization-office-developmen.vercel.app",
        "https://value-realization-office-development-frontend-o0zgqmahs.vercel.app",
    ],
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

# add the new columns to the users table if it was created earlier without them
with engine.begin() as c:
    c.execute(text("ALTER TABLE users ADD COLUMN IF NOT EXISTS name VARCHAR"))
    c.execute(text("ALTER TABLE users ADD COLUMN IF NOT EXISTS role VARCHAR DEFAULT 'Benefit Owner'"))

security = HTTPBearer()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class RegisterData(BaseModel):
    name: str
    email: str
    password: str
    role: str = "Benefit Owner"


class LoginData(BaseModel):
    email: str
    password: str


def create_token(user_id: int) -> str:
    payload = {
        "sub": str(user_id),
        "exp": datetime.now(timezone.utc) + timedelta(hours=8),
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(
    creds: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
):
    try:
        data = jwt.decode(creds.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        user = db.get(models.User, int(data["sub"]))
    except (jwt.PyJWTError, ValueError, KeyError):
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    return user


@app.get("/")
def home():
    return {"message": "VRO backend is running"}


@app.get("/db-check")
def db_check():
    with engine.connect() as c:
        c.execute(text("SELECT 1"))
    return {"database": "connected"}


@app.post("/auth/register")
def register(data: RegisterData, db: Session = Depends(get_db)):
    email = data.email.strip().lower()
    if "@" not in email:
        raise HTTPException(status_code=400, detail="Enter a valid email")
    if len(data.password) < 6 or len(data.password.encode()) > 72:
        raise HTTPException(status_code=400, detail="Password must be 6 to 72 characters")
    if data.role not in ROLES:
        raise HTTPException(status_code=400, detail="Invalid role")
    if db.query(models.User).filter(models.User.email == email).first():
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed = bcrypt.hashpw(data.password.encode(), bcrypt.gensalt()).decode()
    user = models.User(name=data.name.strip(), email=email, password_hash=hashed, role=data.role)
    db.add(user)
    db.commit()
    return {"message": "User registered"}


@app.post("/auth/login")
def login(data: LoginData, db: Session = Depends(get_db)):
    email = data.email.strip().lower()
    user = db.query(models.User).filter(models.User.email == email).first()
    if user is None or len(data.password.encode()) > 72 or not bcrypt.checkpw(
        data.password.encode(), user.password_hash.encode()
    ):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    return {
        "token": create_token(user.id),
        "name": user.name,
        "email": user.email,
        "role": user.role,
    }


@app.get("/auth/me")
def me(user: models.User = Depends(get_current_user)):
    return {"name": user.name, "email": user.email, "role": user.role}