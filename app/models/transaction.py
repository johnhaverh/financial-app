# app/models/transaction.py
"""
Immutable transaction record using dataclass.
"""

from dataclasses import dataclass, field
from datetime import datetime


@dataclass(frozen=True)
class Transaction:
    """Immutable transaction record."""
    amount: float
    type: str  # "deposit" or "withdraw"
    timestamp: datetime = field(default_factory=datetime.utcnow)

    def __post_init__(self):
        if self.amount <= 0:
            raise ValueError("Transaction amount must be positive")
        if self.type not in ("deposit", "withdraw"):
            raise ValueError("Invalid transaction type")