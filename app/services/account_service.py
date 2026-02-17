# app/services/account_service.py
"""
In-memory account service using efficient Python data structures.
For learning purposes before introducing database layer.
"""

from typing import Dict, List, Optional, Set


class AccountService:
    """Manages accounts and transactions in memory."""

    def __init__(self):
        # Main storage: account_id -> account dict
        self._accounts: Dict[str, Dict] = {}
        # Quick lookup for existing IDs (O(1) check)
        self._account_ids: Set[str] = set()

    def create_account(self, account_id: str, initial_balance: float = 0.0) -> Dict:
        """
        Create a new account.
        
        Args:
            account_id: Unique account identifier
            initial_balance: Starting balance
            
        Returns:
            Created account data
            
        Raises:
            ValueError: If account already exists
        """
        if account_id in self._account_ids:
            raise ValueError(f"Account {account_id} already exists")

        account = {
            "id": account_id,
            "balance": initial_balance,
            "transactions": []  # list to keep chronological order
        }
        self._accounts[account_id] = account
        self._account_ids.add(account_id)
        return account

    def get_account(self, account_id: str) -> Optional[Dict]:
        """Get account by ID or None if not found."""
        return self._accounts.get(account_id)

    def list_all_accounts(self) -> List[Dict]:
        """Return a list of all accounts (summary view)."""
        return [
            {"id": acc["id"], "balance": acc["balance"]}
            for acc in self._accounts.values()
        ]

    def add_transaction(self, account_id: str, amount: float, transaction_type: str = "deposit") -> Dict:
        """
        Add deposit or withdraw transaction and update balance.
        
        Args:
            account_id: Target account
            amount: Positive amount
            transaction_type: 'deposit' or 'withdraw'
            
        Returns:
            Updated account
            
        Raises:
            ValueError: Invalid account, amount or type
        """
        account = self.get_account(account_id)
        if not account:
            raise ValueError(f"Account {account_id} not found")

        if amount <= 0:
            raise ValueError("Amount must be positive")

        if transaction_type == "deposit":
            account["balance"] += amount
        elif transaction_type == "withdraw":
            if account["balance"] < amount:
                raise ValueError("Insufficient funds")
            account["balance"] -= amount
        else:
            raise ValueError(f"Invalid transaction type: {transaction_type}")

        # Append to list (maintains insertion order)
        account["transactions"].append({
            "amount": amount,
            "type": transaction_type
        })

        return account

    def get_transactions(self, account_id: str) -> List[Dict]:
        """Get full transaction history for an account."""
        account = self.get_account(account_id)
        if not account:
            raise ValueError(f"Account {account_id} not found")
        return account["transactions"]

    def search_transactions_by_amount(self, account_id: str, min_amount: float) -> List[Dict]:
        """
        Find transactions >= min_amount using list comprehension.
        
        Example: search_transactions_by_amount("ACC-001", 40.0)
        """
        transactions = self.get_transactions(account_id)
        return [tx for tx in transactions if tx["amount"] >= min_amount]

    def get_balance(self, account_id: str) -> float:
        """Current balance of the account."""
        account = self.get_account(account_id)
        if not account:
            raise ValueError(f"Account {account_id} not found")
        return account["balance"]


# Quick demo / test (to run directly)
if __name__ == "__main__":
    service = AccountService()

    # Create accounts
    service.create_account("ACC-001", 200.0)
    service.create_account("ACC-002", 50.0)

    # Transactions
    service.add_transaction("ACC-001", 100.0, "deposit")
    service.add_transaction("ACC-001", 45.0, "withdraw")
    service.add_transaction("ACC-001", 300.0, "deposit")

    # Show results
    print("All accounts:", service.list_all_accounts())
    print("Balance ACC-001:", service.get_balance("ACC-001"))
    print("Transactions ACC-001:", service.get_transactions("ACC-001"))
    print("Large transactions (>= 100):", service.search_transactions_by_amount("ACC-001", 100.0))