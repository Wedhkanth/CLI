import argparse
from pathlib import Path

from pantry.inventory import (
    add_item,
    update_item,
    list_items,
    search_items,
    remove_item,
    inventory_summary,
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

    add_parser = commands.add_parser(
        "add",
        help="Add an ingredient.",
    )
    add_parser.add_argument("name")
    add_parser.add_argument("quantity")
    add_parser.add_argument("unit")
    add_parser.add_argument(
        "--expiry",
        help="Expiry date in YYYY-MM-DD format.",
    )

    update_parser = commands.add_parser(
        "update",
        help="Update an ingredient.",
    )
    update_parser.add_argument("name")
    update_parser.add_argument("quantity")
    update_parser.add_argument("unit")
    update_parser.add_argument(
        "--expiry",
        help="New expiry date in YYYY-MM-DD format.",
    )

    commands.add_parser("list", help="List ingredients.")

    search_parser = commands.add_parser(
        "search",
        help="Search ingredients.",
    )
    search_parser.add_argument("query")

    remove_parser = commands.add_parser(
        "remove",
        help="Remove an ingredient.",
    )
    remove_parser.add_argument("name")

    summary_parser = commands.add_parser(
        "summary",
        help="Show inventory and expiry summary.",
    )
    summary_parser.add_argument(
        "--days",
        type=int,
        default=7,
        help="Days ahead to check for expiry (default: 7).",
    )

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
                args.expiry,
            )
            save_items(args.file, items)

            expiry = (
                item.expiry_date.isoformat()
                if item.expiry_date
                else "Not recorded"
            )

            print(
                f"Added {item.name}: "
                f"{item.quantity:g} {item.unit} "
                f"(Expiry: {expiry})"
            )

        elif args.command == "update":
            item = update_item(
                items,
                args.name,
                args.quantity,
                args.unit,
                args.expiry,
            )
            save_items(args.file, items)

            expiry = (
                item.expiry_date.isoformat()
                if item.expiry_date
                else "Not recorded"
            )

            print(
                f"Updated {item.name}: "
                f"{item.quantity:g} {item.unit} "
                f"(Expiry: {expiry})"
            )

        elif args.command == "list":
            if not items:
                print("Inventory is empty.")
            else:
                for item in list_items(items):
                    expiry = (
                        item.expiry_date.isoformat()
                        if item.expiry_date
                        else "Not recorded"
                    )
                    print(
                        f"{item.name}: "
                        f"{item.quantity:g} {item.unit} "
                        f"(Expiry: {expiry})"
                    )

        elif args.command == "search":
            matches = search_items(items, args.query)

            if not matches:
                print("No matching ingredients found.")
            else:
                for item in matches:
                    expiry = (
                        item.expiry_date.isoformat()
                        if item.expiry_date
                        else "Not recorded"
                    )
                    print(
                        f"{item.name}: "
                        f"{item.quantity:g} {item.unit} "
                        f"(Expiry: {expiry})"
                    )

        elif args.command == "remove":
            item = remove_item(items, args.name)
            save_items(args.file, items)
            print(f"Removed {item.name}.")

        elif args.command == "summary":
            summary = inventory_summary(
                items,
                days=args.days,
            )

            print("\n=== Pantry Inventory Dashboard ===")
            print(f"Total ingredients: {summary['total_items']}")
            print(f"Expired items: {len(summary['expired'])}")
            print(
                f"Expiring today: "
                f"{len(summary['expiring_today'])}"
            )
            print(
                f"Expiring within {args.days} days: "
                f"{len(summary['expiring_soon'])}"
            )
            print(
                f"Missing expiry dates: "
                f"{len(summary['missing_expiry'])}"
            )

            print("\nAll ingredients:")

            if not items:
                print("Inventory is empty.")
            else:
                for item in list_items(items):
                    expiry = (
                        item.expiry_date.isoformat()
                        if item.expiry_date
                        else "Not recorded"
                    )
                    print(
                        f"- {item.name}: "
                        f"{item.quantity:g} {item.unit} "
                        f"(Expiry: {expiry})"
                    )

            sections = [
                ("Expired ingredients", summary["expired"]),
                (
                    "Ingredients expiring today",
                    summary["expiring_today"],
                ),
                ("Upcoming expiries", summary["expiring_soon"]),
                (
                    "Ingredients without expiry dates",
                    summary["missing_expiry"],
                ),
            ]

            for title, matches in sections:
                if matches:
                    print(f"\n{title}:")
                    for item in matches:
                        expiry = (
                            item.expiry_date.isoformat()
                            if item.expiry_date
                            else "Not recorded"
                        )
                        print(
                            f"- {item.name}: "
                            f"{item.quantity:g} {item.unit} "
                            f"(Expiry: {expiry})"
                        )

        return 0

    except (ValueError, OSError) as error:
        print(f"Error: {error}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())