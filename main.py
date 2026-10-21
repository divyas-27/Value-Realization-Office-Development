from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from database import engine, Base
import models

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

@app.get("/")
def home():
    return {"message": "VRO backend is running"}

@app.get("/db-check")
def db_check():
    with engine.connect() as c:
        c.execute(text("SELECT 1"))
    return {"database": "connected"}