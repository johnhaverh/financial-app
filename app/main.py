# app/main.py
from fastapi import FastAPI, HTTPException, Path, Body, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from pydantic import BaseModel, Field, PositiveFloat
from datetime import timedelta

from app.services.account_service import AccountService
from app.exceptions import AccountNotFoundError, InsufficientFundsError, DuplicateAccountError
from app.core.security import verify_password, get_password_hash, create_access_token
from app.core.config import settings
from app.schemas.token import Token, TokenData
from app.schemas.user import User, UserInDB
from app.schemas.account import AccountCreate, DepositRequest, WithdrawRequest, TransferRequest

app = FastAPI(
    title="Financial App API",
    description="RESTful API for managing financial accounts and transactions",
    version="0.1.0",
)

# Fake users DB (in-memory, replace with real DB later)
fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": get_password_hash("secret123"),  # hashed
        "disabled": False,
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice Wonderland",
        "email": "alice@example.com",
        "hashed_password": get_password_hash("wonderland456"),
        "disabled": True,
    },
}

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)

def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        sub = payload.get("sub")
        if sub is None or not isinstance(sub, str):
            raise credentials_exception
        username: str = sub
    except JWTError:
        raise credentials_exception

    user = get_user(fake_users_db, username=username)
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

# Instancia del servicio in-memory
account_service = AccountService()

@app.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends()
):
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        user.username, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/accounts")
def list_accounts(current_user: User = Depends(get_current_active_user)):
    return account_service.list_all_accounts()

@app.post("/accounts", status_code=201)
def create_account(account: AccountCreate, current_user: User = Depends(get_current_active_user)):
    try:
        created = account_service.create_account(account.id, account.initial_balance)
        return {"id": created.id, "balance": created.balance}
    except DuplicateAccountError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/accounts/{account_id}")
def get_account(account_id: str = Path(...), current_user: User = Depends(get_current_active_user)):
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
def deposit(account_id: str = Path(...), req: DepositRequest = Body(...), current_user: User = Depends(get_current_active_user)):
    try:
        acc = account_service.deposit(account_id, req.amount)
        return {"balance": acc.balance}
    except AccountNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/accounts/{account_id}/withdraw")
def withdraw(account_id: str = Path(...), req: WithdrawRequest = Body(...), current_user: User = Depends(get_current_active_user)):
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
def transfer(account_id: str = Path(...), req: TransferRequest = Body(...), current_user: User = Depends(get_current_active_user)):
    try:
        account_service.transfer(account_id, req.to_account_id, req.amount)
        return {"message": f"Transferred {req.amount} from {account_id} to {req.to_account_id}"}
    except AccountNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except InsufficientFundsError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))