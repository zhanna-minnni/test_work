from sqlalchemy.ext.asyncio import AsyncSession
from .models import Wallet


async def get_wallet(db: AsyncSession, wallet_uuid: str):
    return await db.get(Wallet, wallet_uuid)


async def update_balance(db: AsyncSession, wallet_uuid: str, amount: float):
    wallet = await db.get(Wallet, wallet_uuid)
    if wallet:
        wallet.balance += amount
        await db.commit()
        await db.refresh(wallet)
    return wallet