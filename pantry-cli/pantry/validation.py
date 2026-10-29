
import re


pattern= re.compile(r"^[A-Za-z0-9][A-Za-z0-9 '\-]*$")

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
