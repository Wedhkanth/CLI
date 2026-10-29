import json

import pytest

from pantry.models import InventoryItem
from pantry.storage import (
    write_csv,
    read_csv,
    write_json,
    read_json,
)


@pytest.fixture
def sample_items():
    return [
        InventoryItem("Bread Flour", 20.0, "kg"),
        InventoryItem("Sugar", 5.0, "kg"),
    ]


def test_csv_round_trip(tmp_path, sample_items):
    file_path = tmp_path / "inventory.csv"

    write_csv(file_path, sample_items)
    loaded = read_csv(file_path)

    assert loaded == sample_items


def test_json_round_trip(tmp_path, sample_items):
    file_path = tmp_path / "inventory.json"

    write_json(file_path, sample_items)
    loaded = read_json(file_path)

    assert loaded == sample_items


def test_read_missing_csv_returns_empty_list(tmp_path):
    assert read_csv(tmp_path / "missing.csv") == []


def test_read_missing_json_returns_empty_list(tmp_path):
    assert read_json(tmp_path / "missing.json") == []


def test_csv_has_expected_headers(tmp_path, sample_items):
    file_path = tmp_path / "inventory.csv"

    write_csv(file_path, sample_items)
    loaded = read_csv(file_path)

    assert len(loaded) == 2
    assert loaded[0].name == "Bread Flour"


def test_invalid_json_is_rejected(tmp_path):
    file_path = tmp_path / "inventory.json"
    file_path.write_text("{invalid json", encoding="utf-8")

    with pytest.raises(ValueError, match="Could not read JSON inventory"):
        read_json(file_path)


def test_json_with_wrong_structure_is_rejected(tmp_path):
    file_path = tmp_path / "inventory.json"
    file_path.write_text(
        json.dumps({"name": "Sugar"}),
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="must be a list"):
        read_json(file_path)


def test_csv_with_wrong_headers_is_rejected(tmp_path):
    file_path = tmp_path / "inventory.csv"
    file_path.write_text(
        "ingredient,amount\nSugar,5\n",
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="missing required columns"):
        read_csv(file_path)