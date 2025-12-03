import pytest
from pydantic import ValidationError
from typing import List
from backend.app.schemas.admin import (PromoteUser, ApplyPenalty, Admin, ProductOfWeekSelection, ApplyDiscount,)

def test_promote_user_valid():
    obj = PromoteUser(user_id=10)
    assert obj.user_id == 10

def test_promote_user_invalid_type():
    with pytest.raises(ValidationError):
        PromoteUser(user_id="not-int")

def test_apply_penalty_valid():
    obj = ApplyPenalty(
        user_id=1,
        reason="Spamming",
        amount=25.5,
        status="active"
    )
    assert obj.user_id == 1
    assert obj.reason == "Spamming"
    assert obj.amount == 25.5
    assert obj.status == "active"

def test_apply_penalty_missing_field():
    with pytest.raises(ValidationError):
        ApplyPenalty(user_id=1, reason="Late", amount=10.0)

def test_apply_penalty_wrong_type():
    with pytest.raises(ValidationError):
        ApplyPenalty(
            user_id="abc",
            reason=123,
            amount="ten",
            status=5
        )

def test_admin_valid():
    obj = Admin(admin_id=5, username="root", password="secret")
    assert obj.admin_id == 5
    assert obj.username == "root"

def test_admin_missing_field():
    with pytest.raises(ValidationError):
        Admin(admin_id=1, username="no_password")

def test_admin_invalid_types():
    with pytest.raises(ValidationError):
        Admin(admin_id="id", username=123, password=456)

def test_pow_valid():
    obj = ProductOfWeekSelection(product_ids=[1, 2, 3])
    assert obj.product_ids == [1, 2, 3]

def test_pow_empty_list():
    obj = ProductOfWeekSelection(product_ids=[])
    assert obj.product_ids == []

def test_pow_wrong_type():
    with pytest.raises(ValidationError):
        ProductOfWeekSelection(product_ids="not-a-list")

def test_apply_discount_valid():
    obj = ApplyDiscount(product_id=10, discount_percent=20.0)
    assert obj.product_id == 10
    assert obj.discount_percent == 20.0

def test_apply_discount_missing_field():
    with pytest.raises(ValidationError):
        ApplyDiscount(product_id=1)

def test_apply_discount_invalid_types():
    with pytest.raises(ValidationError):
        ApplyDiscount(product_id="id", discount_percent="twenty")
