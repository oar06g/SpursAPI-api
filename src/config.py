from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
import os

class Config:
  def __init__(self):
    load_dotenv()
    self.username = os.getenv('USERNAME')
    self.password = os.getenv('PASSWORD')
    self.database = os.getenv('DATABASE')
    self.host = os.getenv('HOST')
    self.port = os.getenv('PORT')
    self.encryption_password = os.getenv('ENCRYPTION_PASSWORD')

    self.database_url = self._create_database_url()
    self.engine = self._create_engine()
    self.session = self._create_session()


  def _create_database_url(self):
    return f"mysql+aiomysql://{self.username}:{self.password}@{self.host}:{self.port}/{self.database}"
  def _create_engine(self):
    return create_async_engine(self.database_url, echo=True, future=True)
  def _create_session(self):
    return sessionmaker(self.engine, class_=AsyncSession, expire_on_commit=False)
  

config = Config()
SessionLocal = config.session
engine = config.engine

async def get_db():
  async with SessionLocal() as db:
    try:
      yield db
    finally:
      await db.close()