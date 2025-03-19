from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from .database import SessionLocal
from .models import Wallet
from .crud import get_wallet, update_balance
from .schemas import WalletOperation


router = APIRouter()


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        await db.close()


@router.post("/wallets/{wallet_uuid}/operation")
async def wallet_operation(wallet_uuid: str, operation: WalletOperation, db: AsyncSession = Depends(get_db)):
    wallet = await get_wallet(db, wallet_uuid)
    if not wallet:
        raise HTTPException(status_code=404, detail="Wallet not found")

    if operation.operation_type == "DEPOSIT":
        await update_balance(db, wallet_uuid, operation.amount)
    elif operation.operation_type == "WITHDRAW":
        if wallet.balance >= operation.amount:
            await update_balance(db, wallet_uuid, -operation.amount)
        else:
            raise HTTPException(status_code=400, detail="Insufficient funds")
    else:
        raise HTTPException(status_code=400, detail="Invalid operation type")

    return {"message": "Operation successful"}


@router.get("/wallets/{wallet_uuid}")
async def get_wallet_balance(wallet_uuid: str, db: AsyncSession = Depends(get_db)):
    wallet = await get_wallet(db, wallet_uuid)
    if not wallet:
        raise HTTPException(status_code=404, detail="Wallet not found")
    return {"uuid": wallet.uuid, "balance": wallet.balance}