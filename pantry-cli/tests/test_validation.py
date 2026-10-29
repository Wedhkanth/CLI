import pytest

from pantry.validation import (
    validate_name,
    validate_quantity,
    validate_unit,
)


def test_valid_name():
    assert validate_name("Bread Flour") == "Bread Flour"


def test_blank_name_is_rejected():
    with pytest.raises(ValueError):
        validate_name("   ")


def test_valid_quantity():
    assert validate_quantity("2.5") == 2.5


@pytest.mark.parametrize("quantity", ["abc", "0", "-2", "nan", "inf"])
def test_invalid_quantity_is_rejected(quantity):
    with pytest.raises(ValueError):
        validate_quantity(quantity)


def test_unit_is_normalized():
    assert validate_unit("KG") == "kg"


def test_invalid_unit_is_rejected():
    with pytest.raises(ValueError):
        validate_unit("bucket")