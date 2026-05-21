"""
food_utils.py — FridgeBuddy 🥕
Pure-logic helpers: days remaining, status labels, sorting, emoji detection.
No Streamlit imports — keeps this layer clean and unit-testable.
"""

from datetime import date, datetime
from typing import Optional


# ── Days remaining ─────────────────────────────────────────────────────────────

def days_left(expiry_date_str: str) -> Optional[int]:
    """
    Return integer days until expiry (negative = already expired).
    Returns None if the date string is malformed.
    """
    try:
        expiry = datetime.strptime(expiry_date_str, "%Y-%m-%d").date()
        return (expiry - date.today()).days
    except (ValueError, TypeError):
        return None


# ── Status labels ──────────────────────────────────────────────────────────────

def get_status_label(days: Optional[int]) -> str:
    """
    Human-friendly status string based on days remaining.
    Handles None gracefully so bad data never crashes the UI.
    """
    if days is None:
        return "⚠️ Unknown date"
    if days < 0:
        return f"💀 Expired {abs(days)} day{'s' if abs(days) != 1 else ''} ago"
    if days == 0:
        return "🔥 Expires TODAY"
    if days == 1:
        return "⚡ Expires TOMORROW"
    if days <= 2:
        return f"😬 Expires in {days} days"
    if days <= 5:
        return f"🟡 {days} days left"
    if days <= 14:
        return f"🟢 {days} days left"
    return f"✅ {days} days left — all good!"


def get_urgency_level(days: Optional[int]) -> str:
    """
    Classify item into urgency buckets for styling / filtering.
    Returns: 'expired' | 'critical' | 'warning' | 'ok'
    """
    if days is None:
        return "ok"
    if days < 0:
        return "expired"
    if days <= 2:
        return "critical"
    if days <= 5:
        return "warning"
    return "ok"


# ── Sorting ────────────────────────────────────────────────────────────────────

def sort_by_expiry(foods: list[dict]) -> list[dict]:
    """
    Sort food items so the soonest-expiring (or most-expired) comes first.
    Items with unparsable dates are pushed to the end.
    """
    def sort_key(item):
        d = days_left(item.get("expiry_date", ""))
        # None → treat as very far future so it sinks to the bottom
        return d if d is not None else 9999

    return sorted(foods, key=sort_key)


# ── Emoji auto-detection ───────────────────────────────────────────────────────

# Map of keyword fragments → emoji.  Order matters: more specific first.
EMOJI_MAP = {
    "apple": "🍎",   "banana": "🍌",   "orange": "🍊",   "grape": "🍇",
    "strawberr": "🍓", "watermelon": "🍉", "mango": "🥭",  "peach": "🍑",
    "pear": "🍐",    "cherry": "🍒",   "lemon": "🍋",   "lime": "🍋",
    "blueberr": "🫐", "raspberr": "🍓", "avocado": "🥑", "pineapple": "🍍",
    "coconut": "🥥",  "kiwi": "🥝",

    "carrot": "🥕",  "broccoli": "🥦", "spinach": "🥬", "lettuce": "🥬",
    "tomato": "🍅",  "cucumber": "🥒", "pepper": "🫑",  "onion": "🧅",
    "garlic": "🧄",  "potato": "🥔",  "corn": "🌽",    "mushroom": "🍄",
    "celery": "🥬",  "cabbage": "🥬", "zucchini": "🥒",

    "milk": "🥛",    "cheese": "🧀",  "butter": "🧈",  "yogurt": "🫙",
    "egg": "🥚",     "cream": "🥛",

    "chicken": "🍗", "beef": "🥩",    "pork": "🥓",    "fish": "🐟",
    "salmon": "🐟",  "shrimp": "🍤",  "tuna": "🐟",    "meat": "🥩",
    "bacon": "🥓",   "sausage": "🌭", "tofu": "🫙",

    "bread": "🍞",   "rice": "🍚",    "pasta": "🍝",   "noodle": "🍜",
    "pizza": "🍕",   "burger": "🍔",  "sandwich": "🥪",

    "cake": "🎂",    "cookie": "🍪",  "chocolate": "🍫", "candy": "🍬",
    "ice cream": "🍦", "donut": "🍩",

    "juice": "🧃",   "soda": "🥤",    "water": "💧",   "coffee": "☕",
    "tea": "🍵",     "beer": "🍺",    "wine": "🍷",    "milk tea": "🧋",

    "leftover": "🍱", "soup": "🍲",   "salad": "🥗",   "sauce": "🫙",
    "jam": "🫙",      "honey": "🍯",  "oil": "🫙",     "vinegar": "🫙",
}

CATEGORY_DEFAULT_EMOJI = {
    "Fruits 🍎": "🍎",
    "Vegetables 🥦": "🥦",
    "Dairy 🥛": "🥛",
    "Snacks 🍪": "🍪",
    "Drinks 🧃": "🧃",
    "Frozen ❄️": "❄️",
    "Leftovers 🍱": "🍱",
}


def detect_emoji(food_name: str, category: str) -> str:
    """
    Attempt to match the food name against EMOJI_MAP keywords (case-insensitive).
    Falls back to the category default emoji if no match is found.
    """
    name_lower = food_name.lower()
    for keyword, emoji in EMOJI_MAP.items():
        if keyword in name_lower:
            return emoji
    # Category fallback
    return CATEGORY_DEFAULT_EMOJI.get(category, "🍽️")


# ── Dashboard stats ────────────────────────────────────────────────────────────

def compute_stats(foods: list[dict]) -> dict:
    """
    Return a summary dict used by the mascot section and metrics row.
    """
    total = len(foods)
    expiring_soon = []
    expired = []

    for f in foods:
        d = days_left(f.get("expiry_date", ""))
        level = get_urgency_level(d)
        if level == "critical":
            expiring_soon.append(f)
        elif level == "expired":
            expired.append(f)

    return {
        "total": total,
        "expiring_soon": expiring_soon,
        "expired": expired,
        # Simple gamified counter: every non-expiring, non-expired item counts
        "waste_prevented": max(0, total - len(expired)),
    }
