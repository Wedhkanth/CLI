import re
from datetime import date

pattern = re.compile(r"^[A-Za-z0-9][A-Za-z0-9 '’-]*$")

units = {"kg", "g", "l", "ml", "pcs"}


def validate_name(name: str) -> str:
    name = name.strip()

    if not name:
        raise ValueError("Ingredient name cannot be blank.")

    if not pattern.fullmatch(name):
        raise ValueError(
            "Ingredient name may contain only letters, numbers, "
            "spaces, apostrophes, and hyphens."
        )

    return name


def validate_quantity(quantity: str | int | float) -> float:
    try:
        value = float(quantity)
    except (ValueError, TypeError):
        raise ValueError("Quantity must be a number.") from None

    if value <= 0 or not value < float("inf"):
        raise ValueError("Quantity must be greater than zero.")

    return value


def validate_unit(unit: str) -> str:
    if not isinstance(unit, str):
        raise ValueError("Unit must be text.")

    unit = unit.strip().lower()

    if unit not in units:
        raise ValueError(
            "Invalid unit. Allowed units: kg, g, l, ml, pcs."
        )

    return unit


def validate_expiry_date(value: str | date | None) -> date | None:
    if value is None or value == "":
        return None

    if isinstance(value, date):
        return value

    if not isinstance(value, str):
        raise ValueError("Expiry date must use YYYY-MM-DD format.")

    try:
        return date.fromisoformat(value.strip())
    except ValueError:
        raise ValueError(
            "Invalid expiry date. Use YYYY-MM-DD format."
        ) from None