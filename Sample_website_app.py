```python
import streamlit as st
from datetime import date, datetime
import json
import os
import random

# ════════════════════════════════════════════════
# PAGE CONFIG
# ════════════════════════════════════════════════
st.set_page_config(
    page_title="FridgeBuddy 🥕",
    page_icon="🥕",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ════════════════════════════════════════════════
# STORAGE
# ════════════════════════════════════════════════
DATA_FILE = "fridge_data.json"

def load_foods():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as f:
                return json.load(f)
        except:
            return []
    return []

def save_foods(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

if "foods" not in st.session_state:
    st.session_state.foods = load_foods()

# ════════════════════════════════════════════════
# FOOD DATA
# ════════════════════════════════════════════════
CATEGORY_EMOJIS = {
    "Fruits 🍎": "🍎",
    "Vegetables 🥦": "🥦",
    "Dairy 🥛": "🥛",
    "Snacks 🍪": "🍪",
    "Drinks 🧃": "🧃",
    "Frozen ❄️": "❄️",
    "Leftovers 🍱": "🍱",
}

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
    "tomato": "🍅",
    "potato": "🥔",
    "onion": "🧅",
    "garlic": "🧄"
}

def detect_emoji(name, category):
    lower = name.lower()

    for keyword, emoji in EMOJI_MAP.items():
        if keyword in lower:
            return emoji

    return CATEGORY_EMOJIS.get(category, "🍽️")

# ════════════════════════════════════════════════
# HELPERS
# ════════════════════════════════════════════════
def days_left(expiry):
    try:
        expiry_date = datetime.strptime(expiry, "%Y-%m-%d").date()
        return (expiry_date - date.today()).days
    except:
        return 0

def status_text(days):
    if days < 0:
        return f"💀 Expired {abs(days)} day(s) ago"

    if days == 0:
        return "🔥 Expires TODAY"

    if days == 1:
        return "⚡ Expires tomorrow"

    if days <= 3:
        return f"😬 {days} days left"

    return f"✅ {days} days left"

def urgency(days):
    if days < 0:
        return "expired"

    if days <= 2:
        return "critical"

    if days <= 5:
        return "warning"

    return "good"

# ════════════════════════════════════════════════
# FOOD ACTIONS
# ════════════════════════════════════════════════
def add_food(name, category, expiry):
    food = {
        "id": str(datetime.now().timestamp()),
        "name": name,
        "category": category,
        "emoji": detect_emoji(name, category),
        "expiry": expiry.strftime("%Y-%m-%d")
    }

    st.session_state.foods.append(food)
    save_foods(st.session_state.foods)

def delete_food(food_id):
    st.session_state.foods = [
        f for f in st.session_state.foods
        if f["id"] != food_id
    ]

    save_foods(st.session_state.foods)

# ════════════════════════════════════════════════
# SORTING
# ════════════════════════════════════════════════
foods = sorted(
    st.session_state.foods,
    key=lambda x: days_left(x["expiry"])
)

expired = [
    f for f in foods
    if days_left(f["expiry"]) < 0
]

expiring = [
    f for f in foods
    if 0 <= days_left(f["expiry"]) <= 2
]

# ════════════════════════════════════════════════
# CSS
# ════════════════════════════════════════════════
st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800;900&display=swap');

html, body, [class*="css"] {
    font-family: 'Nunito', sans-serif;
}

#MainMenu, footer {
    visibility: hidden;
}

.block-container {
    padding-top: 2rem;
}

.stApp {
    background:
        linear-gradient(
            135deg,
            #fff7ec,
            #ffe5bf,
            #ffd18f
        );
}

/* HEADINGS */

h1, h2, h3 {
    color: #070A3C !important;
}

p, label {
    color: #333 !important;
}

/* SIDEBAR */

section[data-testid="stSidebar"] {
    background:
        linear-gradient(
            180deg,
            #070A3C,
            #062375
        ) !important;
}

section[data-testid="stSidebar"] * {
    color: white !important;
}

/* INPUTS */

.stTextInput input,
.stDateInput input {
    background: white !important;
    color: #222 !important;
    border-radius: 16px !important;
    border: 2px solid rgba(240,102,42,0.2) !important;
}

/* SELECTBOX */

.stSelectbox > div > div {
    background: white !important;
    border-radius: 16px !important;
    border: 2px solid rgba(240,102,42,0.2) !important;
}

/* SELECTED TEXT */

.stSelectbox div[data-baseweb="select"] span {
    color: #222 !important;
    font-weight: 700 !important;
}

/* DROPDOWN */

div[data-baseweb="popover"] {
    background: #fff7ef !important;
    border-radius: 16px !important;
    border: 2px solid rgba(240,102,42,0.2) !important;
}

/* OPTIONS */

div[role="option"] {
    background: transparent !important;
    color: #222 !important;
    font-weight: 700 !important;
    border-radius: 10px !important;
    margin: 4px !important;
}

/* OPTION HOVER */

div[role="option"]:hover {
    background: rgba(240,102,42,0.15) !important;
    color: #070A3C !important;
}

/* SELECTED OPTION */

div[aria-selected="true"] {
    background: rgba(240,102,42,0.18) !important;
    color: #070A3C !important;
}

/* BUTTONS */

.stButton > button {
    background:
        linear-gradient(
            135deg,
            #F0662A,
            #F6941D
        ) !important;

    color: white !important;
    border: none !important;
    border-radius: 18px !important;
    font-weight: 800 !important;
    box-shadow: 0 4px 10px rgba(240,102,42,0.25) !important;
    transition: 0.2s ease;
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 16px rgba(240,102,42,0.4) !important;
}

/* METRICS */

[data-testid="stMetric"] {
    background: rgba(255,255,255,0.85);
    border-radius: 24px;
    padding: 1.2rem;
    backdrop-filter: blur(10px);
    box-shadow: 0 8px 24px rgba(0,0,0,0.03);
}

/* FOOD CARDS */

.html-food-card {
    border-radius: 20px;
    padding: 1.2rem;
    margin-bottom: 0.5rem;
    box-shadow: 0 6px 14px rgba(0,0,0,0.04);
    display: flex;
    justify-content: space-between;
    align-items: center;
}

/* PROGRESS */

.stProgress > div > div > div > div {
    background:
        linear-gradient(
            90deg,
            #F6941D,
            #F0662A
        ) !important;
}

/* RECIPE BOX */

.recipe-box {
    background:
        linear-gradient(
            135deg,
            #F0662A,
            #F6941D
        );

    padding: 1.5rem;
    border-radius: 24px;
    box-shadow: 0 8px 20px rgba(240,102,42,0.2);
}

.recipe-box * {
    color: white !important;
}

/* MASCOT */

.mascot-box {
    background:
        linear-gradient(
            135deg,
            #070A3C,
            #062375
        );

    padding: 1.5rem;
    border-radius: 24px;
    box-shadow: 0 8px 20px rgba(7,10,60,0.2);
}

.mascot-box * {
    color: white !important;
}

</style>
""", unsafe_allow_html=True)

# ════════════════════════════════════════════════
# SIDEBAR
# ════════════════════════════════════════════════
with st.sidebar:

    st.title("🥕 FridgeBuddy")
    st.caption("your chaotic fridge assistant")

    st.divider()

    add_name = st.text_input(
        "Food Name",
        placeholder="e.g. Tomato, Milk..."
    )

    add_cat = st.selectbox(
        "Category",
        list(CATEGORY_EMOJIS.keys())
    )

    add_expiry = st.date_input(
        "Expiry Date",
        value=date.today()
    )

    if add_name.strip():
        st.info(
            f"Detected emoji: {detect_emoji(add_name, add_cat)}"
        )

    if st.button("🥗 Add to Fridge", use_container_width=True):

        if not add_name.strip():
            st.error("Enter a food name 😭")

        else:
            add_food(
                add_name.strip(),
                add_cat,
                add_expiry
            )

            st.success(f"Added {add_name.strip()}!")
            st.balloons()
            st.rerun()

# ════════════════════════════════════════════════
# TITLE
# ════════════════════════════════════════════════
st.markdown("""
<div style='text-align:center;'>

<h1 style='font-size:4.5rem;font-weight:900;'>
🥕 FridgeBuddy
</h1>

<p style='font-size:1.2rem;font-weight:600;opacity:0.85;'>
keeping your food alive one panic notification at a time
</p>

</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ════════════════════════════════════════════════
# METRICS
# ════════════════════════════════════════════════
c1, c2, c3, c4 = st.columns(4)

c1.metric("📦 Total", len(foods))
c2.metric("🔥 Expiring Soon", len(expiring))
c3.metric("💀 Expired", len(expired))
c4.metric("♻️ Saved", max(0, len(foods) - len(expired)))

st.markdown("<br>", unsafe_allow_html=True)

# ════════════════════════════════════════════════
# FILTERS
# ════════════════════════════════════════════════
f1, f2 = st.columns(2)

with f1:
    selected_category = st.selectbox(
        "Filter Category",
        ["All"] + list(CATEGORY_EMOJIS.keys())
    )

with f2:
    search = st.text_input(
        "🔍 Search",
        placeholder="Search fridge..."
    )

filtered_foods = foods

if selected_category != "All":
    filtered_foods = [
        f for f in filtered_foods
        if f["category"] == selected_category
    ]

if search.strip():
    filtered_foods = [
        f for f in filtered_foods
        if search.strip().lower()
        in f["name"].strip().lower()
    ]

# ════════════════════════════════════════════════
# CLEAR EXPIRED
# ════════════════════════════════════════════════
if expired:

    if st.button(
        "🧹 Clear All Expired Items",
        use_container_width=True
    ):

        st.session_state.foods = [
            f for f in st.session_state.foods
            if days_left(f["expiry"]) >= 0
        ]

        save_foods(st.session_state.foods)

        st.success("Expired items removed!")
        st.rerun()

# ════════════════════════════════════════════════
# FOOD LIST
# ════════════════════════════════════════════════
st.subheader("🧊 Your Fridge")

if len(filtered_foods) == 0:

    st.markdown("""
    <div style='
        text-align:center;
        padding:4rem;
        background:rgba(255,255,255,0.6);
        border-radius:24px;
        border:2px dashed rgba(0,0,0,0.1);
    '>

    <div style='font-size:5rem;'>🫙</div>

    <h2>Your fridge is empty</h2>

    <p>
    Add your first item from the sidebar →
    </p>

    </div>
    """, unsafe_allow_html=True)

else:

    for food in filtered_foods:

        d = days_left(food["expiry"])

        bg = {
            "expired": "#ffe5e5",
            "critical": "#fff0df",
            "warning": "#fff7df",
            "good": "#ffffff"
        }[urgency(d)]

        opacity = "0.65" if urgency(d) == "expired" else "1"

        st.markdown(f"""
        <div
        class="html-food-card"
        style="
            background:{bg};
            border:1px solid rgba(0,0,0,0.05);
            opacity:{opacity};
        ">

        <div>

        <span style="font-size:1.8rem;">
        {food["emoji"]}
        </span>

        <strong style="
            font-size:1.3rem;
            color:#070A3C;
            margin-left:0.5rem;
        ">
        {food["name"]}
        </strong>

        <br>

        <span style="
            font-size:0.85rem;
            color:#666;
        ">
        {food["category"]}
        </span>

        </div>

        <div>

        <span style="
            font-size:1.1rem;
            font-weight:800;
            color:#070A3C;
        ">
        {status_text(d)}
        </span>

        </div>

        </div>
        """, unsafe_allow_html=True)

        col_bar, col_btn = st.columns([5,1])

        with col_bar:
            progress = max(min(d / 14, 1.0), 0.0)
            st.progress(progress)

        with col_btn:
            if st.button(
                "🗑️ Consumed",
                key=food["id"],
                use_container_width=True
            ):
                delete_food(food["id"])
                st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)

# ════════════════════════════════════════════════
# RECIPE + MASCOT
# ════════════════════════════════════════════════
st.markdown("<br>", unsafe_allow_html=True)

c_left, c_right = st.columns(2)

with c_left:

    recipe_messages = [
        "🍳 Omelette arc unlocked.",
        "🥪 Sandwich engineering opportunity detected.",
        "🍚 Fried rice would go hard right now.",
        "🥤 Smoothie time.",
        "🍜 Noodle era activated."
    ]

    st.markdown(f"""
    <div class='recipe-box'>

    <h3>
    👨‍🍳 Recipe Suggestion
    </h3>

    <p style='font-size:1.1rem;font-weight:600;'>
    {random.choice(recipe_messages)}
    </p>

    </div>
    """, unsafe_allow_html=True)

with c_right:

    if len(foods) == 0:
        message = "This fridge got abandoned like a group project 😭"

    else:

        good_messages = [
            "Your fridge is thriving ✨",
            "No food casualties detected 🫡",
            "This fridge has emotional stability."
        ]

        chaos_messages = [
            "Your yogurt is entering its villain arc 😭",
            "Please eat something before it develops consciousness.",
            "The spinach is fighting for its life."
        ]

        message = (
            random.choice(chaos_messages)
            if len(expiring) > 2 or len(expired) > 0
            else random.choice(good_messages)
        )

    st.markdown(f"""
    <div class='mascot-box'>

    <h3>
    🥕 Carrot Says...
    </h3>

    <p style='font-size:1.1rem;font-weight:600;'>
    {message}
    </p>

    </div>
    """, unsafe_allow_html=True)
```
