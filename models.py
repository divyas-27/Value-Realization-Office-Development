from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.sql import func
from database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    created_at = Column(DateTime, server_default=func.now())

class Initiative(Base):
    __tablename__ = "initiatives"
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    target_value = Column(Float, default=0)
    realized_value = Column(Float, default=0)
    status = Column(String, default="planned")
    owner_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, server_default=func.now())