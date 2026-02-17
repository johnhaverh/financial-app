# app/services/account_service.py
"""
In-memory account service using domain models (dataclasses).
"""

from typing import Dict, List, Set

from app.exceptions import AccountNotFoundError, DuplicateAccountError, InsufficientFundsError
from app.models.account import Account
from app.models.transaction import Transaction


class AccountService:
    """Service layer for account operations using in-memory storage."""

    def __init__(self):
        self._accounts: Dict[str, Account] = {}
        self._account_ids: Set[str] = set()

    def create_account(self, account_id: str, initial_balance: float = 0.0) -> Account:
        if account_id in self._account_ids:
            raise DuplicateAccountError(f"Account {account_id} already exists")

        account = Account(id=account_id, balance=initial_balance)
        self._accounts[account_id] = account
        self._account_ids.add(account_id)
        return account

    def get_account(self, account_id: str) -> Account:
        account = self._accounts.get(account_id)
        if not account:
            raise AccountNotFoundError(f"Account {account_id} not found")
        return account

    def list_all_accounts(self) -> List[dict]:
        return [{"id": acc.id, "balance": acc.balance} for acc in self._accounts.values()]

    def deposit(self, account_id: str, amount: float) -> Account:
        account = self.get_account(account_id)
        account.deposit(amount)
        return account

    def withdraw(self, account_id: str, amount: float) -> Account:
        account = self.get_account(account_id)
        account.withdraw(amount)
        return account

    def get_transactions(self, account_id: str) -> List[Transaction]:
        account = self.get_account(account_id)
        return account.transactions

    def search_transactions_by_amount(self, account_id: str, min_amount: float) -> List[Transaction]:
        transactions = self.get_transactions(account_id)
        return [tx for tx in transactions if tx.amount >= min_amount]

    def get_balance(self, account_id: str) -> float:
        account = self.get_account(account_id)
        return account.balance


# Demo
if __name__ == "__main__":
    service = AccountService()

    acc1 = service.create_account("ACC-001", 200.0)
    acc2 = service.create_account("ACC-002", 50.0)

    service.deposit("ACC-001", 100.0)
    service.withdraw("ACC-001", 45.0)
    service.deposit("ACC-001", 300.0)

    print("All accounts:", service.list_all_accounts())
    print("Balance ACC-001:", service.get_balance("ACC-001"))
    print("Transactions ACC-001:", [tx.__dict__ for tx in service.get_transactions("ACC-001")])
    print("Large transactions (>= 100):", [tx.__dict__ for tx in service.search_transactions_by_amount("ACC-001", 100.0)])