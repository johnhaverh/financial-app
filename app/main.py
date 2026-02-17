# app/main.py
from fastapi import FastAPI, HTTPException, Path, Body
from pydantic import BaseModel, Field

from app.services.account_service import AccountService
from app.exceptions import AccountNotFoundError, InsufficientFundsError, DuplicateAccountError
from app.schemas.account import AccountCreate, DepositRequest, TransferRequest, WithdrawRequest

app = FastAPI(
    title="Financial App API",
    description="RESTful API for managing financial accounts and transactions",
    version="0.1.0",
)

# Instancia del servicio in-memory
account_service = AccountService()


class AccountCreate(BaseModel):
    id: str = Field(..., min_length=1)
    initial_balance: float = Field(0.0, ge=0.0)


class DepositRequest(BaseModel):
    amount: float = Field(..., gt=0.0)


class TransferRequest(BaseModel):
    to_account_id: str = Field(..., min_length=1)
    amount: float = Field(..., gt=0.0)


@app.get("/accounts")
def list_accounts():
    return account_service.list_all_accounts()


@app.post("/accounts", status_code=201)
def create_account(account: AccountCreate):
    try:
        created = account_service.create_account(account.id, account.initial_balance)
        return {"id": created.id, "balance": created.balance}
    except DuplicateAccountError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/accounts/{account_id}")
def get_account(account_id: str = Path(...)):
    try:
        acc = account_service.get_account(account_id)
        return {
            "id": acc.id,
            "balance": acc.balance,
            "transactions": [{"amount": t.amount, "type": t.type, "timestamp": t.timestamp.isoformat()} for t in acc.transactions]
        }
    except AccountNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.post("/accounts/{account_id}/deposit")
def deposit(account_id: str = Path(...), req: DepositRequest = Body(...)):
    try:
        acc = account_service.deposit(account_id, req.amount)
        return {"balance": acc.balance}
    except AccountNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/accounts/{account_id}/withdraw")
def withdraw(account_id: str = Path(...), req: DepositRequest = Body(...)):
    try:
        acc = account_service.withdraw(account_id, req.amount)
        return {"balance": acc.balance}
    except AccountNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except InsufficientFundsError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/accounts/{account_id}/transfer")
def transfer(account_id: str = Path(...), req: TransferRequest = Body(...)):    
    try:
        account_service.transfer(account_id, req.to_account_id, req.amount)
        return {"message": f"Transferred {req.amount} from {account_id} to {req.to_account_id}"}
    except AccountNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except InsufficientFundsError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
