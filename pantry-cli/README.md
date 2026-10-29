# Pantry CLI

Pantry is a Python command-line application for managing bakery ingredient
inventory. It supports adding, listing, searching, and removing ingredients,
with data stored in CSV or JSON files.

## Features

- Add ingredients with a name, quantity, and unit.
- List all stored ingredients.
- Search ingredients by name.
- Remove ingredients by name.
- Persist inventory in CSV or JSON format.
- Validate names, quantities, and units.
- Reject duplicate ingredient names.

## Requirements

- Python 3.10 or newer
- pytest for running the test suite

## Setup

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
