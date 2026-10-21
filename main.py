from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
    "http://localhost:5173",
    "https://value-realization-office-development-frontend-o0zgqmahs.vercel.app"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "VRO backend is running"}

import os
from sqlalchemy import create_engine, text

DATABASE_URL = os.getenv("DATABASE_URL")
if DATABASE_URL:
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
engine = create_engine(DATABASE_URL) if DATABASE_URL else None

@app.get("/db-test")
def db_test():
    if engine is None:
        return {"db": "DATABASE_URL not set"}
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
    return {"db": "connected"}