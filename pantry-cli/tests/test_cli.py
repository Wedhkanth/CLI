from pantry.cli import main


def test_add_and_list_item(tmp_path, capsys):
    file_path = tmp_path / "inventory.csv"

    result = main([
        "--file", str(file_path),
        "add", "Bread Flour", "20", "kg",
    ])

    assert result == 0
    assert "Added Bread Flour" in capsys.readouterr().out

    result = main([
        "--file", str(file_path),
        "list",
    ])

    assert result == 0
    assert "Bread Flour: 20 kg" in capsys.readouterr().out


def test_search_item(tmp_path, capsys):
    file_path = tmp_path / "inventory.csv"

    main(["--file", str(file_path), "add", "Sugar", "5", "kg"])
    result = main([
        "--file", str(file_path),
        "search", "sug",
    ])

    assert result == 0
    assert "Sugar: 5 kg" in capsys.readouterr().out


def test_remove_item(tmp_path, capsys):
    file_path = tmp_path / "inventory.csv"

    main(["--file", str(file_path), "add", "Sugar", "5", "kg"])
    result = main([
        "--file", str(file_path),
        "remove", "Sugar",
    ])

    assert result == 0
    assert "Removed Sugar" in capsys.readouterr().out

    main(["--file", str(file_path), "list"])
    assert "Inventory is empty." in capsys.readouterr().out


def test_duplicate_item_returns_error(tmp_path, capsys):
    file_path = tmp_path / "inventory.csv"

    main(["--file", str(file_path), "add", "Sugar", "5", "kg"])
    result = main([
        "--file", str(file_path),
        "add", "Sugar", "2", "kg",
    ])

    assert result == 1
    assert "already exists" in capsys.readouterr().out


def test_remove_missing_item_returns_error(tmp_path, capsys):
    file_path = tmp_path / "inventory.csv"

    result = main([
        "--file", str(file_path),
        "remove", "Butter",
    ])

    assert result == 1
    assert "was not found in inventory" in capsys.readouterr().out


def test_json_cli_persistence(tmp_path, capsys):
    file_path = tmp_path / "inventory.json"

    result = main([
        "--file", str(file_path),
        "add", "Butter", "2.5", "kg",
    ])

    assert result == 0

    main(["--file", str(file_path), "list"])
    assert "Butter: 2.5 kg" in capsys.readouterr().out