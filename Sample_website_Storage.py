"""
storage.py — FridgeBuddy 🥕
Handles all reading and writing to data/foods.json.
Uses os.path for cross-platform compatibility (works on Streamlit Cloud too!).
"""

import json
import os
from datetime import date

# ── Path setup ────────────────────────────────────────────────────────────────
# __file__ resolves to storage.py's location, so data/ sits right next to it.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
DATA_FILE = os.path.join(DATA_DIR, "foods.json")


def _ensure_data_file() -> None:
    """Create data/ directory and foods.json if they don't exist yet."""
    os.makedirs(DATA_DIR, exist_ok=True)
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w") as f:
            json.dump([], f)


def load_foods() -> list[dict]:
    """
    Load all food items from the JSON file.
    Returns a list of dicts, each with keys: id, name, category, emoji, expiry_date.
    """
    _ensure_data_file()
    try:
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
            # Guarantee it's always a list even if the file is malformed
            return data if isinstance(data, list) else []
    except (json.JSONDecodeError, IOError):
        return []


def save_foods(foods: list[dict]) -> None:
    """Persist the full list of food items back to the JSON file."""
    _ensure_data_file()
    with open(DATA_FILE, "w") as f:
        json.dump(foods, f, indent=2, default=str)


def add_food(name: str, category: str, emoji: str, expiry_date: date) -> dict:
    """
    Append a new food item and save.
    Returns the newly created item so the caller can use it immediately.
    """
    foods = load_foods()

    # Generate a simple unique ID (timestamp-based to avoid collisions)
    import time
    new_item = {
        "id": str(int(time.time() * 1000)),
        "name": name.strip(),
        "category": category,
        "emoji": emoji,
        "expiry_date": expiry_date.isoformat(),   # stored as "YYYY-MM-DD" string
    }

    foods.append(new_item)
    save_foods(foods)
    return new_item


def delete_food(food_id: str) -> bool:
    """
    Remove the item with the given id.
    Returns True if something was deleted, False if the id wasn't found.
    """
    foods = load_foods()
    original_count = len(foods)
    foods = [f for f in foods if f.get("id") != food_id]

    if len(foods) < original_count:
        save_foods(foods)
        return True
    return False
