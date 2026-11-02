import csv
import json
from datetime import date
from pathlib import Path

from pantry.models import InventoryItem


CSV_FIELDS = ["name", "quantity", "unit", "expiry_date"]
REQUIRED_FIELDS = ["name", "quantity", "unit"]


def parse_expiry_date(value: str | date | None) -> date | None:
    if value is None or value == "":
        return None

    if isinstance(value, date):
        return value

    try:
        return date.fromisoformat(value)
    except (ValueError, TypeError):
        raise ValueError(
            "Invalid expiry date. Use YYYY-MM-DD format."
        ) from None


def read_csv(path: str | Path) -> list[InventoryItem]:
    file_path = Path(path)

    if not file_path.exists():
        return []

    try:
        with file_path.open("r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)

            if reader.fieldnames is None or not all(
                field in reader.fieldnames for field in REQUIRED_FIELDS
            ):
                raise ValueError("CSV file is missing required columns.")

            items = []

            for row in reader:
                items.append(
                    InventoryItem(
                        name=row["name"],
                        quantity=float(row["quantity"]),
                        unit=row["unit"],
                        expiry_date=parse_expiry_date(
                            row.get("expiry_date", "")
                        ),
                    )
                )

            return items

    except (csv.Error, ValueError, TypeError) as error:
        raise ValueError(
            f"Could not read CSV inventory: {error}"
        ) from error


def write_csv(path: str | Path, items: list[InventoryItem]) -> None:
    file_path = Path(path)

    try:
        file_path.parent.mkdir(parents=True, exist_ok=True)

        with file_path.open("w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=CSV_FIELDS)
            writer.writeheader()

            for item in items:
                writer.writerow(
                    {
                        "name": item.name,
                        "quantity": item.quantity,
                        "unit": item.unit,
                        "expiry_date": (
                            item.expiry_date.isoformat()
                            if item.expiry_date
                            else ""
                        ),
                    }
                )

    except OSError as error:
        raise ValueError(
            f"Could not save CSV inventory: {error}"
        ) from error


def read_json(path: str | Path) -> list[InventoryItem]:
    file_path = Path(path)

    if not file_path.exists():
        return []

    try:
        with file_path.open("r", encoding="utf-8") as file:
            data = json.load(file)

        if not isinstance(data, list):
            raise ValueError("JSON inventory must be a list.")

        items = []

        for row in data:
            if not isinstance(row, dict) or not all(
                field in row for field in REQUIRED_FIELDS
            ):
                raise ValueError("JSON item is missing required fields.")

            items.append(
                InventoryItem(
                    name=row["name"],
                    quantity=float(row["quantity"]),
                    unit=row["unit"],
                    expiry_date=parse_expiry_date(
                        row.get("expiry_date")
                    ),
                )
            )

        return items

    except (json.JSONDecodeError, ValueError, TypeError) as error:
        raise ValueError(
            f"Could not read JSON inventory: {error}"
        ) from error


def write_json(path: str | Path, items: list[InventoryItem]) -> None:
    file_path = Path(path)

    data = [
        {
            "name": item.name,
            "quantity": item.quantity,
            "unit": item.unit,
            "expiry_date": (
                item.expiry_date.isoformat()
                if item.expiry_date
                else None
            ),
        }
        for item in items
    ]

    try:
        file_path.parent.mkdir(parents=True, exist_ok=True)

        with file_path.open("w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)

    except OSError as error:
        raise ValueError(
            f"Could not save JSON inventory: {error}"
        ) from error