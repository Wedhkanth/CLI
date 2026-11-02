from datetime import date, timedelta

from pantry.models import InventoryItem
from pantry.validation import (
    validate_name,
    validate_quantity,
    validate_unit,
    validate_expiry_date,
)


def add_item(
    items: list[InventoryItem],
    name: str,
    quantity: str | int | float,
    unit: str,
    expiry_date: str | date | None = None,
) -> InventoryItem:
    name = validate_name(name)
    quantity = validate_quantity(quantity)
    unit = validate_unit(unit)
    expiry_date = validate_expiry_date(expiry_date)

    if any(item.name.casefold() == name.casefold() for item in items):
        raise ValueError(f"'{name}' already exists in inventory.")

    item = InventoryItem(name, quantity, unit, expiry_date)
    items.append(item)
    return item


def update_item(
    items: list[InventoryItem],
    name: str,
    quantity: str | int | float,
    unit: str,
    expiry_date: str | date | None = None,
) -> InventoryItem:
    name = validate_name(name)
    quantity = validate_quantity(quantity)
    unit = validate_unit(unit)

    for index, item in enumerate(items):
        if name.casefold() == item.name.casefold():
            if expiry_date is None:
                expiry_date = item.expiry_date
            else:
                expiry_date = validate_expiry_date(expiry_date)

            updated_item = InventoryItem(
                item.name,
                quantity,
                unit,
                expiry_date,
            )
            items[index] = updated_item
            return updated_item

    raise ValueError(f"Item '{name}' not found.")


def list_items(items: list[InventoryItem]) -> list[InventoryItem]:
    return list(items)


def search_items(
    items: list[InventoryItem],
    query: str,
) -> list[InventoryItem]:
    query = query.strip().casefold()

    if not query:
        raise ValueError("Search query cannot be blank.")

    return [
        item for item in items
        if query in item.name.casefold()
    ]


def remove_item(
    items: list[InventoryItem],
    name: str,
) -> InventoryItem:
    name = validate_name(name)

    for index, item in enumerate(items):
        if item.name.casefold() == name.casefold():
            return items.pop(index)

    raise ValueError(f"'{name}' was not found in inventory.")


def inventory_summary(
    items: list[InventoryItem],
    days: int = 7,
    today: date | None = None,
) -> dict:
    if days < 0:
        raise ValueError("Days cannot be negative.")

    if today is None:
        today = date.today()

    expired = []
    expiring_today = []
    expiring_soon = []
    missing_expiry = []

    end_date = today + timedelta(days=days)

    for item in items:
        if item.expiry_date is None:
            missing_expiry.append(item)
        elif item.expiry_date < today:
            expired.append(item)
        elif item.expiry_date == today:
            expiring_today.append(item)
        elif today < item.expiry_date <= end_date:
            expiring_soon.append(item)

    return {
        "total_items": len(items),
        "expired": expired,
        "expiring_today": expiring_today,
        "expiring_soon": expiring_soon,
        "missing_expiry": missing_expiry,
    }