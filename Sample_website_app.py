import streamlit as st
from datetime import date, datetime
import json
import os
import random

# ════════════════════════════════════════════════
# PAGE CONFIG
# ════════════════════════════════════════════════
st.set_page_config(
    page_title="FridgeBuddy",
    page_icon="🥕",
    layout="wide",
    initial_sidebar_state="collapsed"
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
# THEMES
# ════════════════════════════════════════════════
THEMES = {
    "Sunset Kitchen": {
        "bg1": "#FFF7ED",
        "bg2": "#FFE7C7",
        "primary": "#F0662A",
        "secondary": "#F6941D",
        "dark": "#070A3C",
        "card": "#FFFFFF",
        "text": "#1E293B"
    },
    "Midnight Fridge Raid": {
        "bg1": "#0F172A",
        "bg2": "#111827",
        "primary": "#8B5CF6",
        "secondary": "#6366F1",
        "dark": "#F8FAFC",
        "card": "#1E293B",
        "text": "#F8FAFC"
    },
    "Strawberry Milk": {
        "bg1": "#FFF1F2",
        "bg2": "#FFE4E6",
        "primary": "#FB7185",
        "secondary": "#FDA4AF",
        "dark": "#881337",
        "card": "#FFFFFF",
        "text": "#4C0519"
    }
}

# ════════════════════════════════════════════════
# MASCOTS
# ════════════════════════════════════════════════
MASCOTS = {
    "Carrot 🥕": {
        "emoji": "🥕",
        "good": [
            "Your fridge is thriving bestie.",
            "No food casualties today.",
            "We are so unbelievably back."
        ],
        "bad": [
            "Your yogurt is entering its villain arc.",
            "Please eat something before it gains sentience.",
            "The spinach is fighting for its life."
        ]
    },
    "Frog 🐸": {
        "emoji": "🐸",
        "good": [
            "You’re doing amazing sweetie.",
            "Tiny fridge victories matter too.",
            "Your vegetables feel appreciated."
        ],
        "bad": [
            "Oopsie. The milk is scared.",
            "Maybe we save the strawberries today?",
            "The lettuce believes in you."
        ]
    },
    "Cat 🐈": {
        "emoji": "🐈",
        "good": [
            "Acceptable.",
            "You avoided disaster. Barely.",
            "Hm. Competent."
        ],
        "bad": [
            "Pathetic.",
            "Your fridge smells like consequences.",
            "I’ve seen raccoons organize food better."
        ]
    }
}

# ════════════════════════════════════════════════
# SIDEBAR SETTINGS
# ════════════════════════════════════════════════
with st.sidebar:
    st.title("⚙️ Fridge Settings")

    selected_theme = st.selectbox(
        "Choose Theme",
        list(THEMES.keys())
    )

    selected_mascot = st.selectbox(
        "Choose Mascot",
        list(MASCOTS.keys())
    )

theme = THEMES[selected_theme]
mascot = MASCOTS[selected_mascot]

# ════════════════════════════════════════════════
# CSS
# ════════════════════════════════════════════════
st.markdown(f"""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {{
    font-family: 'Inter', sans-serif;
}}

#MainMenu {{
    visibility: hidden;
}}

footer {{
    visibility: hidden;
}}

.stApp {{
    background:
    linear-gradient(
        135deg,
        {theme["bg1"]},
        {theme["bg2"]}
    );
}}

.block-container {{
    padding-top: 2rem;
    padding-bottom: 5rem;
    max-width: 1200px;
}}

.hero-card {{
    background: rgba(255,255,255,0.7);
    backdrop-filter: blur(16px);
    border-radius: 28px;
    padding: 2.5rem;
    border: 1px solid rgba(255,255,255,0.5);
    box-shadow: 0 8px 30px rgba(0,0,0,0.06);
}}

.title {{
    font-size: 4rem;
    font-weight: 800;
    color: {theme["dark"]};
    line-height: 1;
}}

.subtitle {{
    color: #64748B;
    font-size: 1.1rem;
    margin-top: 0.5rem;
}}

.glass-card {{
    background: rgba(255,255,255,0.7);
    backdrop-filter: blur(14px);
    border-radius: 24px;
    padding: 1.2rem;
    border: 1px solid rgba(255,255,255,0.4);
    box-shadow: 0 8px 20px rgba(0,0,0,0.05);
    margin-bottom: 1rem;
}}

.food-name {{
    font-size: 1.2rem;
    font-weight: 700;
    color: {theme["text"]};
}}

.food-status {{
    font-size: 0.95rem;
    color: #64748B;
}}

.metric-card {{
    background: rgba(255,255,255,0.7);
    border-radius: 24px;
    padding: 1.2rem;
    text-align: center;
    backdrop-filter: blur(14px);
    border: 1px solid rgba(255,255,255,0.5);
}}

.metric-value {{
    font-size: 2rem;
    font-weight: 800;
    color: {theme["dark"]};
}}

.metric-label {{
    color: #64748B;
}}

.floating-mascot {{
    position: fixed;
    bottom: 20px;
    right: 20px;
    width: 280px;
    background: {theme["card"]};
    border-radius: 28px;
    padding: 1.2rem;
    box-shadow: 0 10px 35px rgba(0,0,0,0.12);
    z-index: 999;
    animation: floaty 3s ease-in-out infinite;
}}

@keyframes floaty {{
    0% {{ transform: translateY(0px); }}
    50% {{ transform: translateY(-6px); }}
    100% {{ transform: translateY(0px); }}
}}

.mascot-face {{
    font-size: 3rem;
}}

.mascot-text {{
    font-size: 0.95rem;
    color: #475569;
    margin-top: 0.5rem;
}}

.stButton > button {{
    background: linear-gradient(
        135deg,
        {theme["primary"]},
        {theme["secondary"]}
    ) !important;

    color: white !important;
    border: none !important;
    border-radius: 18px !important;
    height: 3rem !important;
    font-weight: 700 !important;
    transition: 0.2s ease;
}}

.stButton > button:hover {{
    transform: translateY(-2px);
}}

.stTextInput input,
.stDateInput input,
.stSelectbox div[data-baseweb="select"] {{
    border-radius: 16px !important;
    border: none !important;
    background: rgba(255,255,255,0.9) !important;
}}

</style>
""", unsafe_allow_html=True)

# ════════════════════════════════════════════════
# FOOD DATA
# ════════════════════════════════════════════════
CATEGORYS = [
    "Fruits 🍎",
    "Vegetables 🥦",
    "Dairy 🥛",
    "Snacks 🍪",
    "Drinks 🧃",
    "Frozen ❄️"
]

EMOJI_MAP = {
    "apple": "🍎",
    "banana": "🍌",
    "milk": "🥛",
    "pizza": "🍕",
    "bread": "🍞",
    "egg": "🥚",
    "carrot": "🥕",
    "tomato": "🍅",
    "rice": "🍚",
    "cheese": "🧀"
}

def detect_emoji(name):
    lower = name.lower()

    for word, emoji in EMOJI_MAP.items():
        if word in lower:
            return emoji

    return "🍽️"

# ════════════════════════════════════════════════
# HELPERS
# ════════════════════════════════════════════════
def days_left(expiry):
    expiry_date = datetime.strptime(expiry, "%Y-%m-%d").date()
    return (expiry_date - date.today()).days

def add_food(name, category, expiry):
    food = {
        "id": str(datetime.now().timestamp()),
        "name": name,
        "category": category,
        "emoji": detect_emoji(name),
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
# HERO SECTION
# ════════════════════════════════════════════════
st.markdown(f"""
<div class="hero-card">

<div class="title">
🥕 FridgeBuddy
</div>

<div class="subtitle">
your emotionally manipulative fridge companion
</div>

</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ════════════════════════════════════════════════
# ADD FOOD PANEL
# ════════════════════════════════════════════════
st.markdown("### ➕ Add New Food")

col1, col2, col3 = st.columns(3)

with col1:
    add_name = st.text_input(
        "Food Name",
        placeholder="Greek yogurt..."
    )

with col2:
    add_cat = st.selectbox(
        "Category",
        CATEGORYS
    )

with col3:
    add_expiry = st.date_input(
        "Expiry Date",
        value=date.today()
    )

if st.button("Add to Fridge", use_container_width=True):

    if add_name.strip():
        add_food(
            add_name.strip(),
            add_cat,
            add_expiry
        )

        st.success("Added successfully.")
        st.rerun()

# ════════════════════════════════════════════════
# PROCESS DATA
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
    if days_left(f["expiry"]) <= 2
]

# ════════════════════════════════════════════════
# METRICS
# ════════════════════════════════════════════════
m1, m2, m3, m4 = st.columns(4)

metrics = [
    ("Total", len(foods)),
    ("Expiring", len(expiring)),
    ("Expired", len(expired)),
    ("Saved", max(0, len(foods)-len(expired)))
]

for col, metric in zip([m1,m2,m3,m4], metrics):

    with col:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">
                {metric[1]}
            </div>

            <div class="metric-label">
                {metric[0]}
            </div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ════════════════════════════════════════════════
# FOOD LIST
# ════════════════════════════════════════════════
st.markdown("## 🧊 Your Fridge")

if not foods:

    st.markdown("""
    <div class="glass-card" style="text-align:center;">
        <h2>your fridge is empty bestie</h2>
        <p>add something before the carrot gets concerned</p>
    </div>
    """, unsafe_allow_html=True)

else:

    for idx, food in enumerate(foods):

        d = days_left(food["expiry"])

        if d < 0:
            status = f"💀 Expired {abs(d)} day(s) ago"

        elif d == 0:
            status = "🔥 Expires today"

        elif d == 1:
            status = "⚠️ Expires tomorrow"

        else:
            status = f"✅ {d} days left"

        col1, col2 = st.columns([8,1])

        with col1:

            st.markdown(f"""
            <div class="glass-card">

                <div style="
                display:flex;
                justify-content:space-between;
                align-items:center;
                ">

                    <div>
                        <div class="food-name">
                            {food["emoji"]} {food["name"]}
                        </div>

                        <div class="food-status">
                            {food["category"]}
                        </div>
                    </div>

                    <div class="food-status">
                        {status}
                    </div>

                </div>

            </div>
            """, unsafe_allow_html=True)

        with col2:

            if st.button(
                "🗑️",
                key=f"delete_{idx}"
            ):
                delete_food(food["id"])
                st.rerun()

# ════════════════════════════════════════════════
# MASCOT
# ════════════════════════════════════════════════
if len(expired) > 0 or len(expiring) > 2:
    mascot_message = random.choice(mascot["bad"])
else:
    mascot_message = random.choice(mascot["good"])

st.markdown(f"""
<div class="floating-mascot">

<div class="mascot-face">
{mascot["emoji"]}
</div>

<div class="mascot-text">
{mascot_message}
</div>

</div>
""", unsafe_allow_html=True)
