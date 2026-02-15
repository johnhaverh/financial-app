# app/services/account_service.py
"""
In-memory account service for initial development.
This will be replaced/refactored when we connect to real database.
"""

from typing import Dict, List, Optional


class AccountService:
    """Simple in-memory storage for accounts and transactions."""

    def __init__(self):
        # In-memory storage: account_id -> account data
        self._accounts: Dict[str, Dict] = {}

    def create_account(self, account_id: str, initial_balance: float = 0.0) -> Dict:
        """
        Create a new account with given ID and optional initial balance.
        
        Args:
            account_id: Unique identifier for the account
            initial_balance: Starting balance (default 0.0)
            
        Returns:
            The created account dictionary
        """
        if account_id in self._accounts:
            raise ValueError(f"Account {account_id} already exists")
            
        account = {
            "id": account_id,
            "balance": initial_balance,
            "transactions": []
        }
        self._accounts[account_id] = account
        return account

    def get_account(self, account_id: str) -> Optional[Dict]:
        """Retrieve account by ID or return None if not found."""
        return self._accounts.get(account_id)

    def add_transaction(self, account_id: str, amount: float, transaction_type: str = "deposit") -> Dict:
        """
        Add a transaction to an existing account and update balance.
        
        Args:
            account_id: ID of the account
            amount: Transaction amount (positive number)
            transaction_type: 'deposit' or 'withdraw'
            
        Returns:
            Updated account dictionary
            
        Raises:
            ValueError: If account not found or invalid operation
        """
        account = self.get_account(account_id)
        if not account:
            raise ValueError(f"Account {account_id} not found")
            
        if amount <= 0:
            raise ValueError("Transaction amount must be positive")
            
        if transaction_type == "deposit":
            account["balance"] += amount
        elif transaction_type == "withdraw":
            if account["balance"] < amount:
                raise ValueError("Insufficient funds")
            account["balance"] -= amount
        else:
            raise ValueError(f"Invalid transaction type: {transaction_type}")
            
        account["transactions"].append({
            "amount": amount,
            "type": transaction_type
        })
        
        return account

    def get_balance(self, account_id: str) -> float:
        """Get current balance for an account."""
        account = self.get_account(account_id)
        if not account:
            raise ValueError(f"Account {account_id} not found")
        return account["balance"]


# Quick test (remove or move to tests later)
if __name__ == "__main__":
    service = AccountService()
    
    acc = service.create_account("ACC-001", 100.0)
    print(f"Created account: {acc}")
    
    service.add_transaction("ACC-001", 50.0, "deposit")
    service.add_transaction("ACC-001", 30.0, "withdraw")
    
    print(f"Final balance: {service.get_balance('ACC-001')}")
    print(f"Transactions: {service.get_account('ACC-001')['transactions']}")