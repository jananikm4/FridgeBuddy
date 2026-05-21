import streamlit as st
from datetime import date, datetime
from typing import Optional
import random

# ══════════════════════════════════════════════════════════════════════════════
# PAGE CONFIG  (Must be the absolute first Streamlit call)
# ══════════════════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="FridgeBuddy 🥕",
    page_icon="🥕",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ══════════════════════════════════════════════════════════════════════════════
# INTERNAL DATA STORAGE LAYER (Session State Memory)
# ══════════════════════════════════════════════════════════════════════════════
if "fridge_inventory" not in st.session_state:
    st.session_state.fridge_inventory = []

def load_foods() -> list[dict]:
    return st.session_state.fridge_inventory

def add_food(name: str, category: str, emoji: str, expiry_date: date):
    new_item = {
        "id": str(int(datetime.now().timestamp() * 1000)),
        "name": name,
        "category": category,
        "emoji": emoji,
        "expiry_date": expiry_date.strftime("%Y-%m-%d")
    }
    st.session_state.fridge_inventory.append(new_item)

def delete_food(item_id: str):
    st.session_state.fridge_inventory = [
        item for item in st.session_state.fridge_inventory if item["id"] != item_id
    ]

# ══════════════════════════════════════════════════════════════════════════════
# PURE LOGIC HELPERS
# ══════════════════════════════════════════════════════════════════════════════

def days_left(expiry_date_str: str) -> Optional[int]:
    try:
        expiry = datetime.strptime(expiry_date_str, "%Y-%m-%d").date()
        return (expiry - date.today()).days
    except (ValueError, TypeError):
        return None

def get_status_label(days: Optional[int]) -> str:
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
    if days is None:
        return "ok"
    if days < 0:
        return "expired"
    if days <= 2:
        return "critical"
    if days <= 5:
        return "warning"
    return "ok"

def sort_by_expiry(foods_list: list[dict]) -> list[dict]:
    def sort_key(item):
        d = days_left(item.get("expiry_date", ""))
        return d if d is not None else 9999
    return sorted(foods_list, key=sort_key)

# ── Emoji Auto-detection Maps ──
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

def detect_emoji(food_name: str, cat_name: str) -> str:
    name_lower = food_name.lower()
    for keyword, emoji in EMOJI_MAP.items():
        if keyword in name_lower:
            return emoji
    return CATEGORY_DEFAULT_EMOJI.get(cat_name, "🍽️")

def compute_stats(foods_list: list[dict]) -> dict:
    total = len(foods_list)
    expiring_soon = []
    expired = []

    for f in foods_list:
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
        "waste_prevented": max(0, total - len(expired)),
    }

# ══════════════════════════════════════════════════════════════════════════════
# MASCOT MESSAGES
# ══════════════════════════════════════════════════════════════════════════════
HEALTHY_MESSAGES = [
    "Your fridge is absolutely thriving ✨ no food casualties detected 🫡",
    "All items are safe and sound! I'm so proud of you 🥹",
    "Chef's kiss 🤌 — your fridge is living its best life right now.",
    "Zero drama in the fridge today. Seriously impressive fridge management. 💅",
    "Everything is fresh and fine. You deserve a gold star ⭐ — take two.",
]
EXPIRING_TEMPLATES = [
    "Girl PLEASE eat the {name} {emoji} — it's fighting for its life out there 😭",
    "The {name} {emoji} is sending you a distress signal. It deserves better!! 🚨",
    "POV: your {name} {emoji} at 2am wondering why you haven't eaten it yet 🫠",
    "BREAKING: {name} {emoji} is on its last legs. This is not a drill. 😤",
    "{name} {emoji} said 'I thought we were friends' 😔 eat it before it's too late!",
]
EXPIRED_TEMPLATES = [
    "We lost the {name} {emoji} soldier 💔 it has seen things... may it rest in peace 🕯️",
    "Moment of silence for the {name} {emoji} 😔 it deserved better. We all did.",
    "The {name} {emoji} has left the chat 👋 please delete it and move forward.",
    "RIP {name} {emoji} — gone but not forgotten. Mostly just... gone. 🪦",
]
CHAOS_MESSAGES = [
    "Your fridge is living in complete chaos rn 😭 but we love you anyway 💚",
    "Multiple items at risk! This is a Code Green emergency 🚨 (green like the mold haha... sorry 😬)",
    "The fridge is screaming internally. Please. PLEASE eat something. 🥺",
]

def get_mascot_message(stats: dict) -> dict:
    expiring = stats.get("expiring_soon", [])
    expired  = stats.get("expired", [])
    total    = stats.get("total", 0)

    if total == 0:
        return {
            "message": "Hey! Add your first item so I can keep watch 👀 I'm very responsible, I promise.",
            "mood": "happy",
            "tip": "💡 Tip: Start by adding whatever's in your fridge right now — dairy & produce expire fastest!",
        }
    if len(expiring) >= 3 and len(expired) >= 1:
        return {
            "message": random.choice(CHAOS_MESSAGES),
            "mood": "chaos",
            "tip": "💡 Tip: Batch-cook expiring items into one meal to save everything at once!",
        }
    if expired:
        item = expired[0]
        msg = random.choice(EXPIRED_TEMPLATES).format(name=item["name"], emoji=item.get("emoji", "🍽️"))
        return {"message": msg, "mood": "sad", "tip": "💡 Tip: Hit the 🗑️ button to remove expired items and keep your tracker accurate."}
    if expiring:
        item = expiring[0]
        msg = random.choice(EXPIRING_TEMPLATES).format(name=item["name"], emoji=item.get("emoji", "🍽️"))
        return {"message": msg, "mood": "worried", "tip": "💡 Tip: Items expiring within 2 days make great stir-fry, smoothies, or omelettes!"}
    
    return {"message": random.choice(HEALTHY_MESSAGES), "mood": "happy", "tip": "💡 Tip: Keep adding items as you shop so FridgeBuddy can watch over your whole fridge!"}

def get_mood_emoji(mood: str) -> str:
    return {"happy": "😄", "worried": "😰", "sad": "😢", "chaos": "🤯"}.get(mood, "🥕")

# ══════════════════════════════════════════════════════════════════════════════
# REFACTOR INTERACTIVE LAYOUT & SMOOTH TRANSITIONS CSS
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800;900&display=swap');

/* Apply font scaling universally without smashing original input elements */
html, body, [class*="css"] {
    font-family: 'Nunito', sans-serif !important;
}

#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 2rem !important; }

/* ── Clear, High Contrast Metric Blocks ── */
[data-testid="stMetric"] {
    background: #ffffff !important;
    border-radius: 16px !important;
    padding: 1.1rem 1.4rem !important;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05) !important;
    border: 1px solid #eeeeee !important;
    transition: transform 0.2s ease, box-shadow 0.2s ease !important;
}
[data-testid="stMetric"]:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 24px rgba(0, 0, 0, 0.08) !important;
}
[data-testid="stMetricLabel"] { 
    font-weight: 700 !important; 
    color: #666666 !important; 
}
[data-testid="stMetricValue"] > div { 
    font-weight: 900 !important; 
    color: #222222 !important; 
}

/* ── Custom Styled Form Fields ── */
div[data-baseweb="input"], div[data-baseweb="select"] {
    border-radius: 12px !important;
}

/* ── Fluid Interactive Buttons ── */
.stButton > button {
    border-radius: 12px !important;
    font-weight: 700 !important;
    transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
}
.stButton > button:hover {
    border-color: #8fbc8f !important;
    color: #8fbc8f !important;
    background-color: #f0f7f0 !important;
}

/* ── Custom Sidebar Submit Button Accent ── */
[data-testid="stSidebar"] .stButton > button {
    background: linear-gradient(135deg, #8fbc8f, #6aaa6a) !important;
    color: #ffffff !important;
    border: none !important;
    font-weight: 800 !important;
    padding: 0.6rem 1.2rem !important;
    box-shadow: 0 4px 14px rgba(143, 188, 143, 0.3) !important;
}
[data-testid="stSidebar"] .stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 20px rgba(143, 188, 143, 0.45) !important;
    color: #ffffff !important;
    background: linear-gradient(135deg, #99c799, #72b372) !important;
}

hr { border-color: #c8e6c8 !important; }
</style>
""", unsafe_allow_html=True)

# ── Dynamic HTML Card Render Helper ──
def _card_style(urgency: str) -> tuple[str, str]:
    return {
        "expired":  ("#ffeaea", "#ff8a80"),
        "critical": ("#fff8e1", "#ffd97d"),
        "warning":  ("#f0f7f0", "#8fbc8f"),
        "ok":       ("#ffffff", "#eef2ee"),
    }.get(urgency, ("#ffffff", "#eef2ee"))

def render_food_card_html(item: dict, days: int | None) -> str:
    urgency = get_urgency_level(days)
    status  = get_status_label(days)
    bg, border = _card_style(urgency)
    return f"""
    <div style="
        background: {bg}; 
        border: 2px solid {border}; 
        border-radius: 16px; 
        padding: 1rem 1.25rem; 
        margin-bottom: 0.25rem; 
        box-shadow: 0 4px 12px rgba(0,0,0,0.02); 
        display: flex; 
        align-items: center; 
        justify-content: space-between; 
        flex-wrap: wrap; 
        gap: 0.5rem;
    ">
        <div style="display: flex; align-items: center; gap: 0.6rem;">
            <span style="font-size:1.6rem; line-height: 1;">{item.get('emoji','🍽️')}</span>
            <span style="font-size:1.1rem; font-weight:800; color:#2c3e50;">{item['name']}</span>
            <span style="font-size:0.75rem; font-weight:700; background:#f1f2f6; border-radius:20px; padding:3px 12px; color:#57606f;">{item.get('category','').split(' ')[0]}</span>
        </div>
        <div style="font-size:0.95rem; font-weight:700; color:#2c3e50;">{status}</div>
    </div>
    """

# ══════════════════════════════════════════════════════════════════════════════
# SIDEBAR APP INTERACTION LAYOUT
# ══════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("## 🥕 FridgeBuddy")
    st.markdown("*Your cozy fridge companion*")
    st.divider()
    st.markdown("### ➕ Add to Fridge")

    food_name = st.text_input("Food Name", placeholder="e.g. Greek yogurt, Apples…", key="food_name_input")
    category = st.selectbox("Category", options=["Fruits 🍎", "Vegetables 🥦", "Dairy 🥛", "Snacks 🍪", "Drinks 🧃", "Frozen ❄️", "Leftovers 🍱"], key="category_input")
    expiry_date = st.date_input("Expiry Date", value=date.today(), min_value=date(2000, 1, 1), key="expiry_input")

    if food_name.strip():
        detected = detect_emoji(food_name, category)
        st.markdown(f"<div style='font-size:0.85rem; padding-left: 2px; color:#666; margin-top:-0.5rem;'>Detected emoji: {detected}</div>", unsafe_allow_html=True)

    add_clicked = st.button("🥗 Add to Fridge", use_container_width=True)
    if add_clicked:
        if not food_name.strip():
            st.error("Please enter a food name! 🙈")
        else:
            emoji = detect_emoji(food_name.strip(), category)
            add_food(food_name.strip(), category, emoji, expiry_date)
            st.success(f"Added {emoji} {food_name.strip()} to your fridge!")
            st.rerun()

    st.divider()
    st.markdown("<div style='font-size:0.8rem; color:#888; text-align:center;'>Made with 💚 for college students<br>who forget about their food 😅</div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# MAIN VIEWBOARD DASHBOARD
# ══════════════════════════════════════════════════════════════════════════════
foods = load_foods()
sorted_foods = sort_by_expiry(foods)
stats = compute_stats(foods)

st.markdown("""
<div style="text-align:center; padding: 1rem 0 0.5rem 0;">
    <h1 style="font-size:3rem; font-weight:900; margin:0; letter-spacing:-1px;">FridgeBuddy 🥕</h1>
    <p style="font-size:1.1rem; color:#777777; margin-top:0.2rem; font-weight:600;">your friendly fridge assistant — keeping your food (and your wallet) alive ✨</p>
</div>
""", unsafe_allow_html=True)
st.divider()

# Dashboard Stats Row Display
c1, c2, c3, c4 = st.columns(4)
c1.metric("📦 Total Items", stats["total"])
c2.metric("🔥 Expiring Soon", len(stats["expiring_soon"]))
c3.metric("💀 Already Expired", len(stats["expired"]))
c4.metric("♻️ Waste Prevented", f"{stats['waste_prevented']} items")
st.markdown("<br>", unsafe_allow_html=True)

# Expiring Attention Notification Strip
critical_items = [f for f in sorted_foods if get_urgency_level(days_left(f.get("expiry_date", ""))) == "critical"]
if critical_items:
    st.markdown("""
    <div style="background: linear-gradient(135deg, #fff8e1, #ffe8e3); border: 2.5px solid #ffd97d; border-radius: 18px; padding: 1.2rem 1.5rem; margin-bottom: 1.5rem; box-shadow: 0 4px 18px rgba(255,180,0,0.15);">
        <h3 style="margin:0 0 0.6rem 0; color:#b8860b; font-size:1.2rem;">🚨 Eat These NOW — Expiring Within 2 Days!</h3>
    """, unsafe_allow_html=True)
    for item in critical_items:
        days = days_left(item.get("expiry_date", ""))
        status = get_status_label(days)
        st.markdown(f"<div style='display:flex; align-items:center; gap:0.6rem; margin-bottom:0.3rem; font-size:1rem; font-weight:700;'><span style='font-size:1.4rem;'>{item.get('emoji','🍽️')}</span><span>{item['name']}</span><span style='color:#b8860b; font-weight:600;'>— {status}</span></div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# Main Inventory Section
st.markdown("### 🧊 Your Fridge")
if not sorted_foods:
    st.markdown("""
    <div style="text-align:center; padding: 3.5rem 2rem; background: rgba(255,255,255,0.4); border-radius: 20px; border: 2px dashed #dddddd; color: #888888; font-size: 1.1rem;">
        <div style="font-size:3.5rem; margin-bottom: 0.5rem;">🫙</div><strong>Your fridge is empty!</strong><br><span style="color:#aaa; font-size:0.95rem;">Add your first item using the sidebar →</span>
    </div>
    """, unsafe_allow_html=True)
else:
    for item in sorted_foods:
        days = days_left(item.get("expiry_date", ""))
        st.markdown(render_food_card_html(item, days), unsafe_allow_html=True)
        
        # Smooth right-aligned utility line
        main_col, btn_col = st.columns([6, 1])
        with btn_col:
            if st.button("🗑️ Eat/Delete", key=f"del_{item['id']}", use_container_width=True):
                delete_food(item["id"])
                st.rerun()
        st.markdown("<div style='margin-bottom: 0.6rem;'></div>", unsafe_allow_html=True)

# Mascot Interaction Panel
st.divider()
st.markdown("### 🥕 Carrot Says…")
mascot_data = get_mascot_message(stats)
mood_emoji  = get_mood_emoji(mascot_data["mood"])

mood_colors = {"happy": ("#f0f7f0", "#8fbc8f"), "worried": ("#fff8e1", "#ffd97d"), "sad": ("#ffeaea", "#ff8a80"), "chaos": ("#ffe8e3", "#ffb4a2")}
bg_color, border_color = mood_colors.get(mascot_data["mood"], ("#f9f9f9", "#ccc"))

st.markdown(f"""
<div style="background: {bg_color}; border: 2px solid {border_color}; border-radius: 18px; padding: 1.5rem 2rem; display: flex; align-items: flex-start; gap: 1.2rem; box-shadow: 0 4px 16px rgba(0,0,0,0.04);">
    <div style="font-size: 3.5rem; line-height: 1;">{mood_emoji}</div>
    <div>
        <p style="font-size:1.1rem; font-weight:800; margin:0 0 0.5rem 0; color:#2c3e50;">{mascot_data['message']}</p>
        <p style="font-size:0.9rem; color:#7f8c8d; margin:0; font-style:italic;">{mascot_data['tip']}</p>
    </div>
</div>
""", unsafe_allow_html=True)
st.markdown("<br><br>", unsafe_allow_html=True)
