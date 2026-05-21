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
# COLOR PALETTE
# ════════════════════════════════════════════════
HAWKBIT = "#FED46D"
MIMOLETTE = "#F6941D"
ORANGE = "#F0662A"
POHUTUKAWA = "#6A1A29"
BLUE = "#062375"
MIDNIGHT = "#070A3C"

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
# FOOD HELPERS
# ════════════════════════════════════════════════
EMOJI_MAP = {
    "apple": "🍎",
    "banana": "🍌",
    "milk": "🥛",
    "egg": "🥚",
    "bread": "🍞",
    "rice": "🍚",
    "pizza": "🍕",
    "burger": "🍔",
    "carrot": "🥕",
    "broccoli": "🥦",
    "coffee": "☕",
    "tea": "🍵",
    "cake": "🎂",
    "cheese": "🧀",
    "pasta": "🍝",
    "noodle": "🍜",
    "ice cream": "🍦",
    "cookie": "🍪"
}

CATEGORY_EMOJIS = {
    "Fruits 🍎": "🍎",
    "Vegetables 🥦": "🥦",
    "Dairy 🥛": "🥛",
    "Snacks 🍪": "🍪",
    "Drinks 🧃": "🧃",
    "Frozen ❄️": "❄️",
    "Leftovers 🍱": "🍱",
}

def detect_emoji(name, category):
    lower = name.lower()

    for keyword, emoji in EMOJI_MAP.items():
        if keyword in lower:
            return emoji

    return CATEGORY_EMOJIS.get(category, "🍽️")

def days_left(expiry):
    expiry_date = datetime.strptime(expiry, "%Y-%m-%d").date()
    return (expiry_date - date.today()).days

def status_text(days):
    if days < 0:
        return f"💀 Expired {-days} day(s) ago"

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

def add_food(name, category, expiry):
    emoji = detect_emoji(name, category)

    food = {
        "id": str(datetime.now().timestamp()),
        "name": name,
        "category": category,
        "emoji": emoji,
        "expiry": expiry.strftime("%Y-%m-%d")
    }

    st.session_state.foods.append(food)
    save_foods(st.session_state.foods)

def delete_food(food_id):
    st.session_state.foods = [
        food for food in st.session_state.foods
        if food["id"] != food_id
    ]

    save_foods(st.session_state.foods)

# ════════════════════════════════════════════════
# SORT FOOD
# ════════════════════════════════════════════════
foods = sorted(
    st.session_state.foods,
    key=lambda x: days_left(x["expiry"])
)

# ════════════════════════════════════════════════
# STATS
# ════════════════════════════════════════════════
expired = []
expiring = []

for food in foods:
    d = days_left(food["expiry"])

    if d < 0:
        expired.append(food)

    if d <= 2:
        expiring.append(food)

# ════════════════════════════════════════════════
# CSS
# ════════════════════════════════════════════════
st.markdown(f"""
<style>

@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800;900&display=swap');

html, body, [class*="css"] {{
    font-family: 'Nunito', sans-serif;
}}

#MainMenu, footer {{
    visibility: hidden;
}}

.stApp {{
    background:
        linear-gradient(
            135deg,
            #fff6e9,
            #ffe8c5,
            #ffd58f
        );
}}

.block-container {{
    padding-top: 2rem;
}}

h1, h2, h3 {{
    color: {MIDNIGHT} !important;
}

p, span, div, label {{
    color: #333 !important;
}}

section[data-testid="stSidebar"] {{
    background:
        linear-gradient(
            180deg,
            {MIDNIGHT},
            {BLUE}
        );
}}

section[data-testid="stSidebar"] * {{
    color: white !important;
}}

.stTextInput input,
.stDateInput input {{
    background: rgba(255,255,255,0.95) !important;
    color: #222 !important;
    border-radius: 18px !important;
    border: 2px solid rgba(240,102,42,0.2) !important;
}}

.stSelectbox > div > div {{
    background: rgba(255,255,255,0.95) !important;
    color: #222 !important;
    border-radius: 18px !important;
    border: 2px solid rgba(240,102,42,0.2) !important;
}}

.stSelectbox div[data-baseweb="select"] span {{
    color: #222 !important;
    font-weight: 700 !important;
}}

div[role="listbox"] {{
    background: #fff8ef !important;
    border-radius: 18px !important;
}}

div[role="option"] {{
    color: #222 !important;
    font-weight: 700 !important;
    border-radius: 12px !important;
}}

div[role="option"]:hover {{
    background: rgba(240,102,42,0.1) !important;
}}

.stButton > button {{
    background:
        linear-gradient(
            135deg,
            {ORANGE},
            {MIMOLETTE}
        ) !important;

    color: white !important;
    border: none !important;
    border-radius: 18px !important;
    font-weight: 800 !important;
    transition: 0.2s ease;
}}

.stButton > button:hover {{
    transform: translateY(-2px);
    filter: brightness(1.05);
}}

[data-testid="stMetric"] {{
    background: rgba(255,255,255,0.75);
    backdrop-filter: blur(10px);
    border-radius: 28px;
    padding: 1rem;
    box-shadow: 0 8px 22px rgba(0,0,0,0.05);
}}

.food-card {{
    background: rgba(255,255,255,0.75);
    border-radius: 24px;
    padding: 1.2rem;
    margin-bottom: 1rem;
    box-shadow: 0 8px 18px rgba(0,0,0,0.05);
}}

.recipe-box {{
    background:
        linear-gradient(
            135deg,
            {ORANGE},
            {MIMOLETTE}
        );

    padding: 1.5rem;
    border-radius: 24px;
    color: white !important;
    font-weight: 700;
}}

.recipe-box * {{
    color: white !important;
}}

.mascot-box {{
    background:
        linear-gradient(
            135deg,
            {MIDNIGHT},
            {BLUE}
        );

    padding: 1.5rem;
    border-radius: 28px;
}}

.mascot-box * {{
    color: white !important;
}}

.stProgress > div > div > div > div {{
    background:
        linear-gradient(
            90deg,
            {MIMOLETTE},
            {ORANGE}
        ) !important;
}}

::-webkit-scrollbar {{
    width: 10px;
}}

::-webkit-scrollbar-thumb {{
    background: {ORANGE};
    border-radius: 20px;
}}

</style>
""", unsafe_allow_html=True)

# ════════════════════════════════════════════════
# SIDEBAR
# ════════════════════════════════════════════════
with st.sidebar:

    st.title("🥕 FridgeBuddy")
    st.caption("your chaotic fridge assistant")

    st.divider()

    food_name = st.text_input(
        "Food Name",
        placeholder="Greek yogurt..."
    )

    category = st.selectbox(
        "Category",
        list(CATEGORY_EMOJIS.keys())
    )

    expiry = st.date_input(
        "Expiry Date",
        value=date.today()
    )

    if food_name:
        emoji = detect_emoji(food_name, category)
        st.info(f"Detected emoji: {emoji}")

    if st.button("🥗 Add to Fridge", use_container_width=True):

        if food_name.strip() == "":
            st.error("Enter a food name 😭")

        else:
            add_food(food_name, category, expiry)
            st.success(f"Added {food_name}!")
            st.rerun()

    st.divider()

    st.caption("Made with 💛 for students fighting expired milk")

# ════════════════════════════════════════════════
# TITLE
# ════════════════════════════════════════════════
st.markdown(f"""
<div style='text-align:center;'>

<h1 style='
font-size:4.5rem;
font-weight:900;
margin-bottom:0;
'>
🥕 FridgeBuddy
</h1>

<p style='
font-size:1.2rem;
margin-top:0.3rem;
'>
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
f1, f2 = st.columns([1, 1])

with f1:
    filter_category = st.selectbox(
        "Filter Category",
        ["All"] + list(CATEGORY_EMOJIS.keys())
    )

with f2:
    search = st.text_input(
        "🔍 Search",
        placeholder="Search fridge..."
    )

filtered_foods = foods

if filter_category != "All":
    filtered_foods = [
        food for food in filtered_foods
        if food["category"] == filter_category
    ]

if search:
    filtered_foods = [
        food for food in filtered_foods
        if search.lower() in food["name"].lower()
    ]

# ════════════════════════════════════════════════
# CLEAR EXPIRED
# ════════════════════════════════════════════════
if expired:

    if st.button("🧹 Clear All Expired Items"):

        st.session_state.foods = [
            food for food in st.session_state.foods
            if days_left(food["expiry"]) >= 0
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
    <div class='food-card' style='text-align:center;padding:4rem;'>

    <div style='font-size:5rem;'>🫙</div>

    <h2>Your fridge is empty</h2>

    <p>Add your first item from the sidebar →</p>

    </div>
    """, unsafe_allow_html=True)

else:

    for food in filtered_foods:

        d = days_left(food["expiry"])
        status = status_text(d)

        bg = {
            "expired": "#ffe5e5",
            "critical": "#fff0df",
            "warning": "#fff6dc",
            "good": "rgba(255,255,255,0.78)"
        }[urgency(d)]

        st.markdown(f"""
        <div class='food-card' style='background:{bg};'>

        <h3>
        {food["emoji"]} {food["name"]}
        </h3>

        <p style='font-weight:700;'>
        {status}
        </p>

        <p style='color:#666;'>
        {food["category"]}
        </p>

        </div>
        """, unsafe_allow_html=True)

        progress = min(max(d / 14, 0), 1)

        st.progress(progress)

        if st.button(
            "🫡 Consumed",
            key=food["id"],
            use_container_width=True
        ):
            delete_food(food["id"])
            st.rerun()

# ════════════════════════════════════════════════
# RECIPE BOX
# ════════════════════════════════════════════════
st.markdown("<br>", unsafe_allow_html=True)

recipe_messages = [
    "🍳 Omelette arc unlocked.",
    "🥪 Sandwich engineering opportunity detected.",
    "🍚 Fried rice would go hard right now.",
    "🥤 Smoothie time.",
    "🍜 You could absolutely make noodles rn."
]

st.markdown(f"""
<div class='recipe-box'>

<h3 style='margin-top:0;'>
👨‍🍳 Recipe Suggestion
</h3>

<p style='font-size:1.05rem;margin-bottom:0;'>
{random.choice(recipe_messages)}
</p>

</div>
""", unsafe_allow_html=True)

# ════════════════════════════════════════════════
# MASCOT
# ════════════════════════════════════════════════
st.markdown("<br>", unsafe_allow_html=True)

messages_good = [
    "Your fridge is thriving ✨",
    "No food casualties detected 🫡",
    "This fridge has emotional stability."
]

messages_chaos = [
    "Your yogurt is entering its villain arc 😭",
    "Please eat something before it develops consciousness.",
    "The spinach is fighting for its life."
]

message = (
    random.choice(messages_chaos)
    if len(expiring) > 2 or len(expired) > 0
    else random.choice(messages_good)
)

st.markdown(f"""
<div class='mascot-box'>

<h3 style='margin-top:0;'>
🥕 Carrot Says...
</h3>

<p style='font-size:1.1rem;margin-bottom:0;'>
{message}
</p>

</div>
""", unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)
