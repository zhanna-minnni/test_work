from pydantic import BaseModel


class WalletOperation(BaseModel):
    operation_type: str
    amount: float