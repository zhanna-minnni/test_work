import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import SessionLocal
from app.models import Wallet


@pytest.fixture
async def client(db):
    async with TestClient(app) as client:
        yield client


@pytest.fixture
async def wallet(db):
    async with SessionLocal() as session:
        wallet = Wallet(uuid="12345", balance=0.0)
        await session.add(wallet)
        await session.commit()
        yield wallet


async def test_wallet_operation_deposit(client, wallet):
    response = client.post("/wallets/12345/operation", json={"operation_type": "DEPOSIT", "amount": 1000})
    assert response.status_code == 200
    assert response.json() == {"message": "Operation successful"}


async def test_wallet_operation_withdraw(client, wallet):
    response = client.post("/wallets/12345/operation", json={"operation_type": "WITHDRAW", "amount": 500})
    assert response.status_code == 200
    assert response.json() == {"message": "Operation successful"}


async def test_get_wallet_balance(client, wallet):
    response = client.get("/wallets/12345")
    assert response.status_code == 200
    assert response.json() == {"uuid": "12345", "balance": 500}