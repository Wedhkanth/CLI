from dataclasses import dataclass
from datetime import date


@dataclass
class InventoryItem:
    name: str
    quantity: int | float
    unit: str
    expiry_date: date | None = None