import pytest

from pantry.inventory import (
    add_item,
    list_items,
    search_items,
    remove_item,
)


def test_add_item():
    items = []

    item = add_item(items, "Bread Flour", 20, "kg")

    assert item.name == "Bread Flour"
    assert item.quantity == 20.0
    assert len(items) == 1


def test_add_duplicate_item_is_rejected():
    items = []
    add_item(items, "Sugar", 5, "kg")

    with pytest.raises(ValueError, match="already exists"):
        add_item(items, "sugar", 2, "kg")


def test_list_items_returns_copy():
    items = []
    add_item(items, "Sugar", 5, "kg")

    result = list_items(items)

    assert result == items
    assert result is not items


def test_search_items_is_case_insensitive():
    items = []
    add_item(items, "Bread Flour", 20, "kg")

    result = search_items(items, "FLOUR")

    assert len(result) == 1
    assert result[0].name == "Bread Flour"


def test_search_items_rejects_blank_query():
    with pytest.raises(ValueError, match="blank"):
        search_items([], "  ")


def test_search_items_returns_empty_when_not_found():
    items = []
    add_item(items, "Sugar", 5, "kg")

    assert search_items(items, "butter") == []


def test_remove_item_returns_removed_item():
    items = []
    add_item(items, "Sugar", 5, "kg")

    removed = remove_item(items, "sugar")

    assert removed.name == "Sugar"
    assert items == []


def test_remove_missing_item_raises_error():
    with pytest.raises(ValueError, match="not found"):
        remove_item([], "Sugar")