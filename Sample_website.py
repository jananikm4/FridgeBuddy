"""
FridgeBuddy - Single file Streamlit app for Streamlit Cloud
All logic (storage, food utils, mascot) is embedded directly in this file.
Data persists via st.session_state (resets on page refresh - suitable for demo/sample site).
"""

import streamlit as st
import json
import os
import time
from datetime import date, datetime

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="FridgeBuddy",
    page_icon="🥕",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# SESSION STATE INIT
# ─────────────────────────────────────────────
if "foods" not in st.session_state:
    st.session_state.foods = []

if "toast" not in st.session_state:
    st.session_state.toast = None

# ─────────────────────────────────────────────
# GLOBAL CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800;900&display=swap');

html, body, [class*="css"] {
    font-family: 'Nunito', sans-serif !important;
    background-color: #fdf9f3 !important;
    color: #3a3a3a !important;
}

#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 1.5rem !important; padding-bottom: 2rem !important; }

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #eef6ee !important;
    border-right: 2px solid #c8e6c8 !important;
}

/* Add button */
[data-testid="stSidebar"] .stButton > button {
    background: linear-gradient(135deg, #7aaa7a, #5a9a5a) !important;
    color: white !important;
    font-weight: 800 !important;
    font-size: 1rem !important;
    border: none !important;
    border-radius: 14px !important;
    padding: 0.65rem 1.2rem !important;
    width: 100% !important;
    box-shadow: 0 4px 12px rgba(122,170,122,0.4) !important;
    transition: transform 0.15s !important;
}
[data-testid="stSidebar"] .stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 18px rgba(122,170,122,0.55) !important;
}

/* Delete buttons */
.stButton > button {
    border-radius: 8px !important;
    font-family: 'Nunito', sans-serif !important;
    font-weight: 700 !important;
    transition: transform 0.1s !important;
}
.stButton > button:hover { transform: scale(1.04) !important; }

/* Metric cards */
[data-testid="stMetric"] {
    background: white !important;
    border-radius: 14px !important;
    padding: 1rem 1.25rem !important;
    box-shadow: 0 4px 16px rgba(0,0,0,0.06) !important;
    border: 1.5px solid #ececec !important;
}
[data-testid="stMetricLabel"] { font-weight: 700 !important; color: #9a9a9a !important; }
[data-testid="stMetricValue"] { font-weight: 900 !important; }

input, select, textarea {
    border-radius: 10px !important;
    font-family: 'Nunito', sans-serif !important;
}
hr { border-color: #c8e6c8 !important; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# FOOD UTILS
# ─────────────────────────────────────────────

EMOJI_MAP = {
    "apple": "🍎", "banana": "🍌", "orange": "🍊", "grape": "🍇",
    "strawberr": "🍓", "watermelon": "🍉", "mango": "🥭", "peach": "🍑",
    "pear": "🍐", "cherry": "🍒", "lemon": "🍋", "lime": "🍋",
    "blueberr": "🫐", "raspberr": "🍓", "avocado": "🥑", "pineapple": "🍍",
    "coconut": "🥥", "kiwi": "🥝",
    "carrot": "🥕", "broccoli": "🥦", "spinach": "🥬", "lettuce": "🥬",
    "tomato": "🍅", "cucumber": "🥒", "pepper": "🫑", "onion": "🧅",
    "garlic": "🧄", "potato": "🥔", "corn": "🌽", "mushroom": "🍄",
    "celery": "🥬", "cabbage": "🥬", "zucchini": "🥒",
    "milk": "🥛", "cheese": "🧀", "butter": "🧈", "yogurt": "🫙",
    "egg": "🥚", "cream": "🥛",
    "chicken": "🍗", "beef": "🥩", "pork": "🥓", "fish": "🐟",
    "salmon": "🐟", "shrimp": "🍤", "tuna": "🐟", "meat": "🥩",
    "bacon": "🥓", "sausage": "🌭", "tofu": "🫙",
    "bread": "🍞", "rice": "🍚", "pasta": "🍝", "noodle": "🍜",
    "pizza": "🍕", "burger": "🍔", "sandwich": "🥪",
    "cake": "🎂", "cookie": "🍪", "chocolate": "🍫", "candy": "🍬",
    "donut": "🍩", "ice cream": "🍦",
    "juice": "🧃", "soda": "🥤", "water": "💧", "coffee": "☕",
    "tea": "🍵", "beer": "🍺", "wine": "🍷",
    "leftover": "🍱", "soup": "🍲", "salad": "🥗", "sauce": "🫙",
    "jam": "🫙", "honey": "🍯",
}

CATEGORY_EMOJI = {
    "Fruits": "🍎", "Vegetables": "🥦", "Dairy": "🥛",
    "Snacks": "🍪", "Drinks": "🧃", "Frozen": "❄️", "Leftovers": "🍱",
}


def detect_emoji(name: str, category: str) -> str:
    lower = name.lower()
    for keyword, emoji in EMOJI_MAP.items():
        if keyword in lower:
            return emoji
    return CATEGORY_EMOJI.get(category, "🍽️")


def days_left(expiry_date_str: str):
    try:
        expiry = datetime.strptime(expiry_date_str, "%Y-%m-%d").date()
        return (expiry - date.today()).days
    except Exception:
        return None


def get_urgency(days) -> str:
    if days is None:  return "ok"
    if days < 0:      return "expired"
    if days <= 2:     return "critical"
    if days <= 5:     return "warning"
    return "ok"


def get_status_label(days) -> str:
    if days is None: return "Unknown date"
    if days < 0:     return f"💀 Expired {abs(days)} day{'s' if abs(days) != 1 else ''} ago"
    if days == 0:    return "🔥 Expires TODAY"
    if days == 1:    return "⚡ Expires TOMORROW"
    if days <= 2:    return f"😬 Expires in {days} days"
    if days <= 5:    return f"🟡 {days} days left"
    if days <= 14:   return f"🟢 {days} days left"
    return f"✅ {days} days left"


def sort_by_expiry(foods: list) -> list:
    return sorted(foods, key=lambda f: (days_left(f.get("expiry_date", "")) or 9999))


def compute_stats(foods: list) -> dict:
    expiring_soon = [f for f in foods if get_urgency(days_left(f.get("expiry_date", ""))) == "critical"]
    expired       = [f for f in foods if get_urgency(days_left(f.get("expiry_date", ""))) == "expired"]
    return {
        "total": len(foods),
        "expiring_soon": expiring_soon,
        "expired": expired,
        "waste_prevented": max(0, len(foods) - len(expired)),
    }


# ─────────────────────────────────────────────
# MASCOT MESSAGES
# ─────────────────────────────────────────────
import random

HEALTHY_MSGS = [
    "Your fridge is absolutely thriving today no food casualties detected",
    "All items are safe and sound! I'm so proud of you",
    "Chef's kiss — your fridge is living its best life right now.",
    "Zero drama in the fridge today. Seriously impressive fridge management.",
    "Everything is fresh and fine. You deserve a gold star — take two.",
]
EXPIRING_TMPL = [
    lambda n, e: f"Girl PLEASE eat the {n} {e} — it's fighting for its life out there!",
    lambda n, e: f"The {n} {e} is sending you a distress signal. It deserves better!!",
    lambda n, e: f"POV: your {n} {e} at 2am wondering why you haven't eaten it yet",
    lambda n, e: f"BREAKING: {n} {e} is on its last legs. This is not a drill.",
    lambda n, e: f"{n} {e} said 'I thought we were friends' — eat it before it's too late!",
]
EXPIRED_TMPL = [
    lambda n, e: f"We lost the {n} {e} soldier — it has seen things... may it rest in peace",
    lambda n, e: f"Moment of silence for the {n} {e} — it deserved better. We all did.",
    lambda n, e: f"The {n} {e} has left the chat — please delete it and move forward.",
    lambda n, e: f"RIP {n} {e} — gone but not forgotten. Mostly just... gone.",
]
CHAOS_MSGS = [
    "Your fridge is living in complete chaos rn but we love you anyway",
    "Multiple items at risk! Please. PLEASE eat something.",
    "The fridge is screaming internally. This is a Code Green emergency.",
]

def get_mascot(stats: dict) -> dict:
    soon, expired, total = stats["expiring_soon"], stats["expired"], stats["total"]
    if total == 0:
        return {"msg": "Hey! Add your first item so I can keep watch — I'm very responsible, I promise.", "mood": "happy", "tip": "Tip: Start with dairy and produce — they expire fastest!", "face": "😄"}
    if len(soon) >= 3 and len(expired) >= 1:
        return {"msg": random.choice(CHAOS_MSGS), "mood": "chaos", "tip": "Tip: Batch-cook everything expiring into one stir-fry!", "face": "🤯"}
    if expired:
        f = expired[0]
        return {"msg": random.choice(EXPIRED_TMPL)(f["name"], f["emoji"]), "mood": "sad", "tip": "Tip: Hit the delete button to remove expired items and keep your tracker accurate.", "face": "😢"}
    if soon:
        f = soon[0]
        return {"msg": random.choice(EXPIRING_TMPL)(f["name"], f["emoji"]), "mood": "worried", "tip": "Tip: Items expiring within 2 days make great stir-fry, smoothies, or omelettes!", "face": "😰"}
    return {"msg": random.choice(HEALTHY_MSGS), "mood": "happy", "tip": "Tip: Keep adding items as you shop so FridgeBuddy can keep watch!", "face": "😄"}

MOOD_STYLE = {
    "happy":   ("background:#f0f7f0; border:2px solid #8fbc8f;",   "#2e6b2e"),
    "worried": ("background:#fff8e1; border:2px solid #ffd97d;",   "#9a6f00"),
    "sad":     ("background:#ffeaea; border:2px solid #ff8a80;",   "#b02020"),
    "chaos":   ("background:#ffe8e3; border:2px solid #ffb4a2;",   "#8b3a20"),
}

CARD_STYLE = {
    "expired":  ("background:#ffeaea; border:2px solid #ff8a80;"),
    "critical": ("background:#fff8e1; border:2px solid #ffd97d;"),
    "warning":  ("background:#eef6ee; border:2px solid #c8e6c8;"),
    "ok":       ("background:#ffffff; border:2px solid #e8e8e8;"),
}


# ─────────────────────────────────────────────
# SIDEBAR — Add Food Form
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🥕 FridgeBuddy")
    st.markdown("*Your cozy fridge companion*")
    st.divider()
    st.markdown("### Add to Fridge")

    food_name = st.text_input("Food Name", placeholder="e.g. Greek yogurt, Apples...", key="input_name")
    category  = st.selectbox("Category", ["Fruits", "Vegetables", "Dairy", "Snacks", "Drinks", "Frozen", "Leftovers"])
    expiry    = st.date_input("Expiry Date", value=date.today())

    if food_name.strip():
        preview = detect_emoji(food_name, category)
        st.markdown(f"<div style='font-size:0.82rem;color:#888;margin-top:-0.4rem;'>Detected emoji: {preview}</div>", unsafe_allow_html=True)

    if st.button("Add to Fridge", use_container_width=True):
        if not food_name.strip():
            st.error("Please enter a food name!")
        else:
            emoji = detect_emoji(food_name.strip(), category)
            new_item = {
                "id": str(int(time.time() * 1000)),
                "name": food_name.strip(),
                "category": category,
                "emoji": emoji,
                "expiry_date": expiry.isoformat(),
            }
            st.session_state.foods.append(new_item)
            st.session_state.toast = f"Added {emoji} {food_name.strip()} to your fridge!"
            st.rerun()

    if st.session_state.toast:
        st.success(st.session_state.toast)
        st.session_state.toast = None

    st.divider()
    st.markdown(
        "<div style='font-size:0.78rem;color:#aaa;text-align:center;'>"
        "Made with 💚 for college students<br>who forget about their food 😅"
        "</div>",
        unsafe_allow_html=True,
    )


# ─────────────────────────────────────────────
# MAIN DASHBOARD
# ─────────────────────────────────────────────
foods        = st.session_state.foods
sorted_foods = sort_by_expiry(foods)
stats        = compute_stats(foods)

# Header
st.markdown("""
<div style='text-align:center; padding:1rem 0 0.5rem;'>
  <h1 style='font-size:2.8rem; font-weight:900; margin:0; letter-spacing:-1px;'>FridgeBuddy 🥕</h1>
  <p style='font-size:1rem; color:#888; font-weight:600; margin-top:0.3rem;'>
    your friendly fridge assistant — keeping your food (and your wallet) alive ✨
  </p>
</div>
""", unsafe_allow_html=True)

st.divider()

# Metrics
c1, c2, c3, c4 = st.columns(4)
c1.metric("📦 Total Items",     stats["total"])
c2.metric("🔥 Expiring Soon",   len(stats["expiring_soon"]))
c3.metric("💀 Already Expired", len(stats["expired"]))
c4.metric("♻️ Waste Prevented", f"{stats['waste_prevented']} items")

st.markdown("<br>", unsafe_allow_html=True)

# Alert zone
critical_items = [f for f in sorted_foods if get_urgency(days_left(f.get("expiry_date", ""))) == "critical"]
if critical_items:
    alert_rows = "".join([
        f"<div style='display:flex;align-items:center;gap:0.6rem;margin-bottom:0.3rem;font-weight:700;color:#7a5500;'>"
        f"<span style='font-size:1.3rem;'>{f['emoji']}</span>"
        f"<span>{f['name']}</span>"
        f"<span style='font-size:0.85rem;color:#9a6f00;'>— {get_status_label(days_left(f['expiry_date']))}</span>"
        f"</div>"
        for f in critical_items
    ])
    st.markdown(f"""
    <div style='background:linear-gradient(135deg,#fff8e1,#ffe8e3);border:2.5px solid #ffd97d;
                border-radius:18px;padding:1.2rem 1.5rem;margin-bottom:1.5rem;
                box-shadow:0 4px 18px rgba(255,180,0,0.12);'>
      <div style='font-size:1rem;font-weight:800;color:#9a6f00;margin-bottom:0.7rem;'>
        🚨 Eat These NOW — Expiring Within 2 Days!
      </div>
      {alert_rows}
    </div>
    """, unsafe_allow_html=True)

# Food list
st.markdown("### 🧊 Your Fridge")

if not sorted_foods:
    st.markdown("""
    <div style='text-align:center;padding:3rem 2rem;background:#f9f9f9;
                border-radius:18px;border:2px dashed #ccc;color:#aaa;font-size:1rem;'>
      <div style='font-size:3rem;'>🫙</div>
      <strong style='color:#888;display:block;margin:0.5rem 0;'>Your fridge is empty!</strong>
      Add your first item using the sidebar →
    </div>
    """, unsafe_allow_html=True)
else:
    for item in sorted_foods:
        d       = days_left(item.get("expiry_date", ""))
        urgency = get_urgency(d)
        status  = get_status_label(d)
        card_style = CARD_STYLE.get(urgency, CARD_STYLE["ok"])

        col_card, col_btn = st.columns([7, 1])
        with col_card:
            st.markdown(f"""
            <div style='{card_style} border-radius:14px; padding:0.8rem 1.2rem;
                        box-shadow:0 2px 8px rgba(0,0,0,0.04);
                        display:flex; align-items:center; justify-content:space-between;
                        flex-wrap:wrap; gap:0.4rem;'>
              <div style='display:flex;align-items:center;gap:0.6rem;'>
                <span style='font-size:1.5rem;'>{item['emoji']}</span>
                <strong style='font-size:1rem;'>{item['name']}</strong>
                <span style='font-size:0.75rem;background:#f0f0f0;border-radius:20px;
                             padding:2px 10px;color:#777;font-weight:700;'>{item['category']}</span>
              </div>
              <div style='font-size:0.88rem;font-weight:700;color:#666;'>{status}</div>
            </div>
            """, unsafe_allow_html=True)

        with col_btn:
            if st.button("🗑️", key=f"del_{item['id']}", help="Eat / Delete"):
                st.session_state.foods = [f for f in st.session_state.foods if f["id"] != item["id"]]
                st.rerun()

# Mascot section
st.divider()
st.markdown("### 🥕 Carrot Says...")

mascot = get_mascot(stats)
box_style, text_color = MOOD_STYLE.get(mascot["mood"], MOOD_STYLE["happy"])

st.markdown(f"""
<div style='{box_style} border-radius:18px; padding:1.5rem 2rem;
            display:flex; align-items:flex-start; gap:1.2rem;
            box-shadow:0 4px 16px rgba(0,0,0,0.06);'>
  <div style='font-size:3.2rem; line-height:1; flex-shrink:0;'>{mascot['face']}</div>
  <div>
    <p style='font-size:1rem; font-weight:700; margin:0 0 0.5rem; color:{text_color};'>
      {mascot['msg']}
    </p>
    <p style='font-size:0.85rem; color:#888; margin:0; font-style:italic; font-weight:600;'>
      💡 {mascot['tip']}
    </p>
  </div>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
