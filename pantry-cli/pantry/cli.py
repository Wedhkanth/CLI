import argparse
from pathlib import Path

from pantry.inventory import (
    add_item,
    list_items,
    search_items,
    remove_item,
)
from pantry.storage import (
    read_csv,
    write_csv,
    read_json,
    write_json,
)


DEFAULT_FILE = "data/inventory.csv"


def load_items(file_path):
    suffix = Path(file_path).suffix.lower()

    if suffix == ".csv":
        return read_csv(file_path)
    if suffix == ".json":
        return read_json(file_path)

    raise ValueError("Inventory file must end in .csv or .json.")


def save_items(file_path, items):
    suffix = Path(file_path).suffix.lower()

    if suffix == ".csv":
        write_csv(file_path, items)
    elif suffix == ".json":
        write_json(file_path, items)
    else:
        raise ValueError("Inventory file must end in .csv or .json.")


def build_parser():
    parser = argparse.ArgumentParser(
        prog="pantry",
        description="Manage a bakery ingredient inventory.",
    )
    parser.add_argument(
        "--file",
        default=DEFAULT_FILE,
        help="Inventory file (.csv or .json).",
    )

    commands = parser.add_subparsers(
        dest="command",
        required=True,
    )

    add_parser = commands.add_parser("add", help="Add an ingredient.")
    add_parser.add_argument("name")
    add_parser.add_argument("quantity")
    add_parser.add_argument("unit")

    commands.add_parser("list", help="List ingredients.")

    search_parser = commands.add_parser("search", help="Search ingredients.")
    search_parser.add_argument("query")

    remove_parser = commands.add_parser("remove", help="Remove an ingredient.")
    remove_parser.add_argument("name")

    return parser


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        items = load_items(args.file)

        if args.command == "add":
            item = add_item(
                items,
                args.name,
                args.quantity,
                args.unit,
            )
            save_items(args.file, items)
            print(f"Added {item.name}: {item.quantity:g} {item.unit}")

        elif args.command == "list":
            if not items:
                print("Inventory is empty.")
            else:
                for item in list_items(items):
                    print(f"{item.name}: {item.quantity:g} {item.unit}")

        elif args.command == "search":
            matches = search_items(items, args.query)
            if not matches:
                print("No matching ingredients found.")
            else:
                for item in matches:
                    print(f"{item.name}: {item.quantity:g} {item.unit}")

        elif args.command == "remove":
            item = remove_item(items, args.name)
            save_items(args.file, items)
            print(f"Removed {item.name}.")

        return 0

    except (ValueError, OSError) as error:
        print(f"Error: {error}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())