from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from src.config import engine
import datetime
import asyncio

Base = declarative_base()

class User(Base):
  __tablename__ = 'users'
  id = Column(Integer, primary_key=True, index=True)
  full_name = Column(String, index=True)
  email = Column(String, unique=True, index=True)
  password = Column(String)
  created_at = Column(DateTime, default=datetime.datetime.utcnow)
  