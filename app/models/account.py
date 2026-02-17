# app/models/account.py
"""
Data models for Account using dataclasses.
"""

from dataclasses import dataclass, field
from typing import List

from app.exceptions import InsufficientFundsError
from app.models.transaction import Transaction


@dataclass
class Account:
    """Account entity with balance and transaction history."""
    id: str
    balance: float = 0.0
    transactions: List[Transaction] = field(default_factory=list)

    def deposit(self, amount: float) -> None:
        """Add deposit transaction."""
        self.transactions.append(Transaction(amount=amount, type="deposit"))
        self.balance += amount

    def withdraw(self, amount: float) -> None:
        """Add withdraw transaction if funds available."""
        if self.balance < amount:
            raise InsufficientFundsError(f"Insufficient funds: {self.balance} < {amount}")
        self.transactions.append(Transaction(amount=amount, type="withdraw"))
        self.balance -= amount