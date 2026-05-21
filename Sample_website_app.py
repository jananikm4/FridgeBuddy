import streamlit as st
from datetime import date, datetime
from typing import Optional
import random
import json
import os

# ══════════════════════════════════════════════════════════════════════════════
# PAGE CONFIG
# ══════════════════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="FridgeBuddy 🥕",
    page_icon="🥕",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ══════════════════════════════════════════════════════════════════════════════
# COLOR PALETTE
# ══════════════════════════════════════════════════════════════════════════════
PUDDLE = "#6999A1"
THISTLE = "#9295C0"
LAVENDER = "#AB82A4"
PINK = "#F06E95"
CORAL = "#FC9390"
PEACH = "#FEE3CA"

# ══════════════════════════════════════════════════════════════════════════════
# DATA STORAGE
# ══════════════════════════════════════════════════════════════════════════════
DATA_FILE = "fridge_data.json"

def load_foods():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []

def save_foods(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

if "fridge_inventory" not in st.session_state:
    st.session_state.fridge_inventory = load_foods()

def add_food(name: str, category: str, emoji: str, expiry_date: date):
    new_item = {
        "id": str(int(datetime.now().timestamp() * 1000)),
        "name": name,
        "category": category,
        "emoji": emoji,
        "expiry_date": expiry_date.strftime("%Y-%m-%d")
    }

    st.session_state.fridge_inventory.append(new_item)
    save_foods(st.session_state.fridge_inventory)

def delete_food(item_id: str):
    st.session_state.fridge_inventory = [
        item for item in st.session_state.fridge_inventory
        if item["id"] != item_id
    ]
    save_foods(st.session_state.fridge_inventory)

# ══════════════════════════════════════════════════════════════════════════════
# HELPERS
# ══════════════════════════════════════════════════════════════════════════════
def days_left(expiry_date_str: str) -> Optional[int]:
    try:
        expiry = datetime.strptime(expiry_date_str, "%Y-%m-%d").date()
        return (expiry - date.today()).days
    except:
        return None

def get_status_label(days):
    if days is None:
        return "⚠️ Unknown"
    if days < 0:
        return f"💀 Expired {abs(days)} day(s) ago"
    if days == 0:
        return "🔥 Expires TODAY"
    if days == 1:
        return "⚡ Expires TOMORROW"
    if days <= 2:
        return f"😬 {days} days left"
    if days <= 5:
        return f"🟡 {days} days left"

    return f"✅ {days} days left"

def get_urgency_level(days):
    if days is None:
        return "ok"
    if days < 0:
        return "expired"
    if days <= 2:
        return "critical"
    if days <= 5:
        return "warning"

    return "ok"

def sort_by_expiry(food_list):
    return sorted(
        food_list,
        key=lambda x: days_left(x["expiry_date"]) if days_left(x["expiry_date"]) is not None else 9999
    )

# ══════════════════════════════════════════════════════════════════════════════
# EMOJI DETECTION
# ══════════════════════════════════════════════════════════════════════════════
EMOJI_MAP = {
    "apple": "🍎",
    "banana": "🍌",
    "milk": "🥛",
    "egg": "🥚",
    "bread": "🍞",
    "pizza": "🍕",
    "burger": "🍔",
    "rice": "🍚",
    "cake": "🎂",
    "coffee": "☕",
    "tea": "🍵",
    "carrot": "🥕",
    "broccoli": "🥦",
    "cheese": "🧀",
    "pasta": "🍝",
    "noodle": "🍜",
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

def detect_emoji(food_name, category):
    lower = food_name.lower()

    for keyword, emoji in EMOJI_MAP.items():
        if keyword in lower:
            return emoji

    return CATEGORY_DEFAULT_EMOJI.get(category, "🍽️")

# ══════════════════════════════════════════════════════════════════════════════
# STATS
# ══════════════════════════════════════════════════════════════════════════════
def compute_stats(food_list):
    expired = []
    expiring = []

    for item in food_list:
        d = days_left(item["expiry_date"])

        if get_urgency_level(d) == "expired":
            expired.append(item)

        if get_urgency_level(d) == "critical":
            expiring.append(item)

    return {
        "total": len(food_list),
        "expired": expired,
        "expiring": expiring,
        "saved": max(0, len(food_list) - len(expired))
    }

# ══════════════════════════════════════════════════════════════════════════════
# RECIPE SUGGESTIONS
# ══════════════════════════════════════════════════════════════════════════════
def suggest_recipe(items):
    names = [i["name"].lower() for i in items]
    joined = " ".join(names)

    if "egg" in joined:
        return "🍳 Omelette time."
    if "bread" in joined:
        return "🥪 Sandwich opportunity detected."
    if "milk" in joined and "banana" in joined:
        return "🥤 Smoothie arc unlocked."
    if "rice" in joined:
        return "🍚 Fried rice would slap right now."

    return "🍲 Mystery meal challenge activated."

# ══════════════════════════════════════════════════════════════════════════════
# MASCOT MESSAGES
# ══════════════════════════════════════════════════════════════════════════════
GOOD_MESSAGES = [
    "Your fridge is thriving ✨",
    "No food casualties detected 🫡",
    "This fridge has emotional stability.",
]

PANIC_MESSAGES = [
    "Your yogurt is entering its villain arc 😭",
    "The spinach is fighting for its life.",
    "Please eat something before it develops consciousness.",
]

# ══════════════════════════════════════════════════════════════════════════════
# CSS
# ══════════════════════════════════════════════════════════════════════════════
st.markdown(f"""
<style>

@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800;900&display=swap');

html, body, [class*="css"] {{
    font-family: 'Nunito', sans-serif;
    color: #2f2f2f !important;
}}

#MainMenu, footer {{
    visibility: hidden;
}}

.stApp {{
    background: linear-gradient(
        135deg,
        {PEACH},
        #fff7f2,
        #fef3ff
    );
}}

.block-container {{
    padding-top: 2rem;
}}

h1, h2, h3, h4, h5, h6 {{
    color: #3b3b3b !important;
}}

p, label, span, div {{
    color: #444 !important;
}}

section[data-testid="stSidebar"] {{
    background: linear-gradient(
        180deg,
        {PUDDLE},
        {THISTLE}
    );
}}

section[data-testid="stSidebar"] * {{
    color: white !important;
}}

.stTextInput input,
.stSelectbox div[data-baseweb="select"],
.stDateInput input {{
    background: white !important;
    color: #333 !important;
    border-radius: 14px !important;
    border: 2px solid #eee !important;
}}

.stButton > button {{
    background: linear-gradient(
        135deg,
        {PINK},
        {CORAL}
    ) !important;

    color: white !important;
    border: none !important;
    border-radius: 14px !important;
    font-weight: 800 !important;
    transition: 0.2s ease;
    box-shadow: 0 4px 14px rgba(0,0,0,0.12);
}}

.stButton > button:hover {{
    transform: translateY(-2px);
    filter: brightness(1.05);
}}

[data-testid="stMetric"] {{
    background: rgba(255,255,255,0.8);
    border: 2px solid rgba(255,255,255,0.6);
    backdrop-filter: blur(10px);
    border-radius: 24px;
    padding: 1rem;
    box-shadow: 0 6px 18px rgba(0,0,0,0.06);
}}

[data-testid="stMetricLabel"] {{
    color: #555 !important;
    font-weight: 700;
}}

[data-testid="stMetricValue"] {{
    color: #2f2f2f !important;
    font-weight: 900;
}}

.food-card {{
    border-radius: 24px;
    padding: 1.2rem;
    margin-bottom: 1rem;
    background: rgba(255,255,255,0.75);
    backdrop-filter: blur(10px);
    border: 2px solid rgba(255,255,255,0.5);
    box-shadow: 0 6px 18px rgba(0,0,0,0.05);
}}

.recipe-box {{
    background: linear-gradient(
        135deg,
        {LAVENDER},
        {THISTLE}
    );

    color: white !important;
    padding: 1.2rem;
    border-radius: 20px;
    font-weight: 700;
}}

.recipe-box * {{
    color: white !important;
}}

.mascot-box {{
    background: linear-gradient(
        135deg,
        {PINK},
        {CORAL}
    );

    color: white !important;
    padding: 1.5rem;
    border-radius: 24px;
    box-shadow: 0 8px 22px rgba(0,0,0,0.08);
}}

.mascot-box * {{
    color: white !important;
}}

</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════════════════════════════
with st.sidebar:

    st.title("🥕 FridgeBuddy")
    st.caption("your chaotic little fridge assistant")

    st.divider()

    st.subheader("➕ Add Food")

    food_name = st.text_input(
        "Food Name",
        placeholder="Greek yogurt..."
    )

    category = st.selectbox(
        "Category",
        list(CATEGORY_DEFAULT_EMOJI.keys())
    )

    expiry_date = st.date_input(
        "Expiry Date",
        value=date.today()
    )

    if food_name.strip():
        detected = detect_emoji(food_name, category)
        st.info(f"Detected emoji: {detected}")

    if st.button("🥗 Add to Fridge", use_container_width=True):

        if not food_name.strip():
            st.error("Enter a food name 😭")

        else:
            emoji = detect_emoji(food_name, category)

            add_food(
                food_name.strip(),
                category,
                emoji,
                expiry_date
            )

            st.success(f"Added {emoji} {food_name}")
            st.rerun()

    st.divider()

    st.caption("Made with 💚 for students who forget food exists")

# ══════════════════════════════════════════════════════════════════════════════
# MAIN APP
# ══════════════════════════════════════════════════════════════════════════════
foods = load_foods()
sorted_foods = sort_by_expiry(foods)
stats = compute_stats(sorted_foods)

st.markdown(f"""
<div style='text-align:center; margin-bottom:2rem;'>

<h1 style='
font-size:4.5rem;
font-weight:900;
color:{PUDDLE};
margin-bottom:0;
'>
🥕 FridgeBuddy
</h1>

<p style='
font-size:1.2rem;
color:#555;
margin-top:0.4rem;
'>
keeping your food alive one panic notification at a time
</p>

</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# METRICS
# ══════════════════════════════════════════════════════════════════════════════
c1, c2, c3, c4 = st.columns(4)

c1.metric("📦 Total", stats["total"])
c2.metric("🔥 Expiring Soon", len(stats["expiring"]))
c3.metric("💀 Expired", len(stats["expired"]))
c4.metric("♻️ Saved", stats["saved"])

st.markdown("<br>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# FILTERS
# ══════════════════════════════════════════════════════════════════════════════
f1, f2 = st.columns(2)

with f1:
    selected_category = st.selectbox(
        "Filter Category",
        ["All"] + list(CATEGORY_DEFAULT_EMOJI.keys())
    )

with f2:
    search = st.text_input(
        "🔍 Search",
        placeholder="Search fridge..."
    )

if selected_category != "All":
    sorted_foods = [
        f for f in sorted_foods
        if f["category"] == selected_category
    ]

if search:
    sorted_foods = [
        f for f in sorted_foods
        if search.lower() in f["name"].lower()
    ]

# ══════════════════════════════════════════════════════════════════════════════
# DELETE EXPIRED
# ══════════════════════════════════════════════════════════════════════════════
if stats["expired"]:

    if st.button("🧹 Clear All Expired Items"):
        st.session_state.fridge_inventory = [
            item for item in st.session_state.fridge_inventory
            if get_urgency_level(days_left(item["expiry_date"])) != "expired"
        ]

        save_foods(st.session_state.fridge_inventory)

        st.success("Expired items removed.")
        st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
# FRIDGE ITEMS
# ══════════════════════════════════════════════════════════════════════════════
st.subheader("🧊 Your Fridge")

if not sorted_foods:

    st.markdown(f"""
    <div class='food-card' style='text-align:center;padding:4rem;'>

    <div style='font-size:5rem;'>🫙</div>

    <h2 style='color:{PUDDLE};'>
    Your fridge is empty
    </h2>

    <p>
    Add your first item from the sidebar →
    </p>

    </div>
    """, unsafe_allow_html=True)

else:

    for item in sorted_foods:

        days = days_left(item["expiry_date"])
        status = get_status_label(days)

        urgency = get_urgency_level(days)

        bg = {
            "expired": "#ffe5eb",
            "critical": "#fff0e4",
            "warning": "#fff7ea",
            "ok": "rgba(255,255,255,0.75)"
        }[urgency]

        st.markdown(f"""
        <div class='food-card' style='background:{bg};'>

        <h3>
        {item['emoji']} {item['name']}
        </h3>

        <p style='font-weight:700;'>
        {status}
        </p>

        <p style='color:#777;'>
        {item['category']}
        </p>

        </div>
        """, unsafe_allow_html=True)

        progress = 0

        if days is not None:
            progress = min(max(days / 14, 0), 1)

        st.progress(progress)

        if st.button(
            "🫡 Consumed",
            key=item["id"],
            use_container_width=True
        ):
            delete_food(item["id"])
            st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
# RECIPE IDEA
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("<br>", unsafe_allow_html=True)

st.subheader("👨‍🍳 FridgeBuddy Recipe Suggestion")

recipe = suggest_recipe(sorted_foods)

st.markdown(f"""
<div class='recipe-box'>
{recipe}
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# MASCOT
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("<br>", unsafe_allow_html=True)

st.subheader("🥕 Carrot Says")

message = (
    random.choice(PANIC_MESSAGES)
    if len(stats["expired"]) > 0 or len(stats["expiring"]) > 2
    else random.choice(GOOD_MESSAGES)
)

st.markdown(f"""
<div class='mascot-box'>

<h3 style='margin-top:0;'>
🥕 FridgeBuddy has thoughts...
</h3>

<p style='font-size:1.05rem; margin-bottom:0;'>
{message}
</p>

</div>
""", unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)
