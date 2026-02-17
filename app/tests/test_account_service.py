# app/tests/test_account_service.py
"""
Unit tests for AccountService using pytest.
"""

import pytest

from app.exceptions import AccountNotFoundError, DuplicateAccountError, InsufficientFundsError
from app.models.account import Account
from app.models.transaction import Transaction
from app.services.account_service import AccountService


@pytest.fixture
def service():
    """Fixture to create a fresh AccountService for each test."""
    return AccountService()


def test_create_account(service):
    account = service.create_account("ACC-TEST", 100.0)
    assert account.id == "ACC-TEST"
    assert account.balance == 100.0
    assert len(account.transactions) == 0


def test_create_duplicate_account(service):
    service.create_account("ACC-DUP", 50.0)
    with pytest.raises(DuplicateAccountError):
        service.create_account("ACC-DUP", 0.0)


def test_deposit(service):
    acc = service.create_account("ACC-DEP", 0.0)
    service.deposit("ACC-DEP", 200.0)
    assert service.get_balance("ACC-DEP") == 200.0
    assert len(service.get_transactions("ACC-DEP")) == 1
    assert service.get_transactions("ACC-DEP")[0].amount == 200.0
    assert service.get_transactions("ACC-DEP")[0].type == "deposit"


def test_withdraw_success(service):
    service.create_account("ACC-WIT", 300.0)
    service.withdraw("ACC-WIT", 150.0)
    assert service.get_balance("ACC-WIT") == 150.0


def test_withdraw_insufficient(service):
    service.create_account("ACC-INS", 100.0)
    with pytest.raises(InsufficientFundsError):
        service.withdraw("ACC-INS", 200.0)


def test_transfer_success(service):
    service.create_account("ACC-A", 500.0)
    service.create_account("ACC-B", 0.0)
    
    service.transfer("ACC-A", "ACC-B", 200.0)
    
    assert service.get_balance("ACC-A") == 300.0
    assert service.get_balance("ACC-B") == 200.0
    assert len(service.get_transactions("ACC-A")) == 1  # withdraw
    assert len(service.get_transactions("ACC-B")) == 1  # deposit


def test_transfer_same_account(service):
    service.create_account("ACC-SAME", 100.0)
    with pytest.raises(ValueError):
        service.transfer("ACC-SAME", "ACC-SAME", 50.0)


def test_transfer_not_found(service):
    with pytest.raises(AccountNotFoundError):
        service.transfer("NON-EXIST", "ACC-B", 50.0)