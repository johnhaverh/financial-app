# app/exceptions.py
"""
Custom exceptions for the financial application.
"""


class AccountNotFoundError(Exception):
    """Raised when an account is not found."""
    pass


class InsufficientFundsError(Exception):
    """Raised when attempting to withdraw more than available balance."""
    pass


class DuplicateAccountError(Exception):
    """Raised when trying to create an existing account."""
    pass


class InvalidTransactionError(Exception):
    """Raised for invalid transaction types or amounts."""
    pass