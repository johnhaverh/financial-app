# app/schemas/account.py
from pydantic import BaseModel, Field, PositiveFloat, field_validator

class AccountCreate(BaseModel):
    id: str = Field(..., min_length=3, max_length=20, description="Unique account identifier")
    initial_balance: float = Field(0.0, ge=0.0, description="Initial balance >= 0")

    @field_validator("id")
    def id_alphanumeric(cls, v):
        if not v.isalnum():
            raise ValueError("Account ID must be alphanumeric")
        return v


class DepositRequest(BaseModel):
    amount: PositiveFloat = Field(..., gt=0.0, description="Amount must be positive")


class WithdrawRequest(BaseModel):
    amount: PositiveFloat = Field(..., gt=0.0)


class TransferRequest(BaseModel):
    to_account_id: str = Field(..., min_length=3)
    amount: PositiveFloat = Field(..., gt=0.0)