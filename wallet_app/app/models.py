from sqlalchemy import Column, String, Float
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Wallet(Base):
    __tablename__ = "wallets"

    uuid = Column(String, primary_key=True, index=True)
    balance = Column(Float, default=0.0)