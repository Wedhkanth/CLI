
from pantry.models import InventoryItem
from pantry.validation import (
    validate_name,
    validate_quantity,
    validate_unit,
)


def add_item(
    items: list[InventoryItem],
    name: str,
    quantity: str | int | float,
    unit: str,
) -> InventoryItem:
    name = validate_name(name)
    quantity = validate_quantity(quantity)
    unit = validate_unit(unit)

    if any(item.name.casefold() == name.casefold() for item in items):
        raise ValueError(f"'{name}' already exists in inventory.")

    item = InventoryItem(name, quantity, unit)
    items.append(item)
    return item


def list_items(items: list[InventoryItem]) -> list[InventoryItem]:
    return list(items)


def search_items(
    items: list[InventoryItem], query: str
) -> list[InventoryItem]:
    query = query.strip().casefold()

    if not query:
        raise ValueError("Search query cannot be blank.")

    return [
        item for item in items
        if query in item.name.casefold()
    ]


def remove_item(
    items: list[InventoryItem], name: str
) -> InventoryItem:
    name = validate_name(name)

    for index, item in enumerate(items):
        if item.name.casefold() == name.casefold():
            return items.pop(index)

    raise ValueError(f"'{name}' was not found in inventory.")
