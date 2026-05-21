<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>FridgeBuddy 🥕</title>
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link href="https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800;900&display=swap" rel="stylesheet" />
<style>
  /* ── Reset & Root ─────────────────────────────────── */
  *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

  :root {
    --sage:      #7aaa7a;
    --sage-lt:   #c8e6c8;
    --sage-bg:   #eef6ee;
    --cream:     #fdf9f3;
    --peach:     #ffb4a2;
    --peach-lt:  #ffe8e3;
    --yellow:    #ffd97d;
    --yellow-lt: #fff8e1;
    --red-lt:    #ffeaea;
    --red-border:#ff8a80;
    --text:      #3a3a3a;
    --text-mid:  #6b6b6b;
    --text-light:#9a9a9a;
    --white:     #ffffff;
    --radius:    14px;
    --radius-sm: 8px;
    --shadow:    0 4px 20px rgba(0,0,0,0.07);
    --shadow-lg: 0 8px 32px rgba(0,0,0,0.10);
    font-family: 'Nunito', 'Quicksand', sans-serif;
  }

  body {
    background: var(--cream);
    color: var(--text);
    min-height: 100vh;
  }

  /* ── Layout ───────────────────────────────────────── */
  .shell {
    display: grid;
    grid-template-columns: 300px 1fr;
    min-height: 100vh;
  }

  /* ── Sidebar ──────────────────────────────────────── */
  .sidebar {
    background: var(--sage-bg);
    border-right: 2px solid var(--sage-lt);
    padding: 2rem 1.5rem;
    position: sticky;
    top: 0;
    height: 100vh;
    overflow-y: auto;
    display: flex;
    flex-direction: column;
    gap: 1.2rem;
  }

  .sidebar-logo {
    text-align: center;
    padding-bottom: 0.5rem;
  }
  .sidebar-logo h1 {
    font-size: 1.7rem;
    font-weight: 900;
    color: var(--text);
    letter-spacing: -0.5px;
  }
  .sidebar-logo p {
    font-size: 0.82rem;
    color: var(--text-mid);
    margin-top: 0.2rem;
    font-weight: 600;
  }

  .sidebar hr {
    border: none;
    border-top: 1.5px solid var(--sage-lt);
  }

  .form-label {
    display: block;
    font-size: 0.82rem;
    font-weight: 700;
    color: var(--text-mid);
    margin-bottom: 0.35rem;
    text-transform: uppercase;
    letter-spacing: 0.5px;
  }

  .form-input, .form-select {
    width: 100%;
    padding: 0.6rem 0.9rem;
    border: 2px solid var(--sage-lt);
    border-radius: var(--radius-sm);
    background: var(--white);
    font-family: 'Nunito', sans-serif;
    font-size: 0.95rem;
    font-weight: 600;
    color: var(--text);
    outline: none;
    transition: border-color 0.2s;
    appearance: none;
  }
  .form-input:focus, .form-select:focus {
    border-color: var(--sage);
    box-shadow: 0 0 0 3px rgba(122,170,122,0.15);
  }

  .emoji-preview {
    font-size: 0.8rem;
    color: var(--text-light);
    margin-top: 0.3rem;
    min-height: 1.2rem;
  }

  .btn-add {
    width: 100%;
    padding: 0.75rem 1rem;
    background: linear-gradient(135deg, var(--sage), #5a9a5a);
    color: white;
    border: none;
    border-radius: var(--radius);
    font-family: 'Nunito', sans-serif;
    font-size: 1rem;
    font-weight: 800;
    cursor: pointer;
    box-shadow: 0 4px 14px rgba(122,170,122,0.4);
    transition: transform 0.15s, box-shadow 0.15s;
    letter-spacing: 0.2px;
  }
  .btn-add:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(122,170,122,0.5);
  }
  .btn-add:active { transform: translateY(0); }

  .toast {
    padding: 0.65rem 1rem;
    border-radius: var(--radius-sm);
    font-size: 0.88rem;
    font-weight: 700;
    display: none;
    animation: fadeIn 0.3s ease;
  }
  .toast.success { background: #eaf7ea; color: #2e7a2e; border: 1.5px solid #a8dba8; display: block; }
  .toast.error   { background: var(--red-lt); color: #c0392b; border: 1.5px solid var(--red-border); display: block; }

  .sidebar-footer {
    margin-top: auto;
    text-align: center;
    font-size: 0.78rem;
    color: var(--text-light);
    line-height: 1.6;
  }

  /* ── Main ─────────────────────────────────────────── */
  .main {
    padding: 2.5rem 2.5rem 4rem;
    max-width: 860px;
  }

  .page-header {
    text-align: center;
    margin-bottom: 2rem;
  }
  .page-header h1 {
    font-size: 3rem;
    font-weight: 900;
    letter-spacing: -1.5px;
    line-height: 1;
  }
  .page-header p {
    color: var(--text-mid);
    font-size: 1rem;
    font-weight: 600;
    margin-top: 0.4rem;
  }

  /* ── Metrics ──────────────────────────────────────── */
  .metrics {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 0.85rem;
    margin-bottom: 2rem;
  }
  .metric-card {
    background: var(--white);
    border: 1.5px solid #ececec;
    border-radius: var(--radius);
    padding: 1rem 1.2rem;
    box-shadow: var(--shadow);
  }
  .metric-label {
    font-size: 0.75rem;
    font-weight: 700;
    color: var(--text-light);
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-bottom: 0.3rem;
  }
  .metric-value {
    font-size: 1.9rem;
    font-weight: 900;
    color: var(--text);
    line-height: 1;
  }

  /* ── Section headers ──────────────────────────────── */
  .section-title {
    font-size: 1.1rem;
    font-weight: 800;
    color: var(--text);
    margin-bottom: 0.85rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
  }

  /* ── Alert zone ───────────────────────────────────── */
  .alert-zone {
    background: linear-gradient(135deg, var(--yellow-lt), var(--peach-lt));
    border: 2.5px solid var(--yellow);
    border-radius: 18px;
    padding: 1.2rem 1.5rem;
    margin-bottom: 1.8rem;
    box-shadow: 0 4px 18px rgba(255,180,0,0.12);
    animation: fadeIn 0.4s ease;
  }
  .alert-zone-title {
    font-size: 1rem;
    font-weight: 800;
    color: #9a6f00;
    margin-bottom: 0.7rem;
  }
  .alert-item {
    display: flex;
    align-items: center;
    gap: 0.6rem;
    font-size: 0.95rem;
    font-weight: 700;
    margin-bottom: 0.3rem;
    color: #7a5500;
  }

  /* ── Food cards ───────────────────────────────────── */
  .food-list { display: flex; flex-direction: column; gap: 0.6rem; }

  .food-card {
    background: var(--white);
    border: 2px solid #e8e8e8;
    border-radius: var(--radius);
    padding: 0.85rem 1.2rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 1rem;
    box-shadow: 0 2px 10px rgba(0,0,0,0.04);
    transition: transform 0.15s, box-shadow 0.15s;
    animation: slideIn 0.3s ease;
  }
  .food-card:hover {
    transform: translateY(-1px);
    box-shadow: 0 4px 16px rgba(0,0,0,0.08);
  }
  .food-card.urgency-critical {
    background: var(--yellow-lt);
    border-color: var(--yellow);
  }
  .food-card.urgency-expired {
    background: var(--red-lt);
    border-color: var(--red-border);
    opacity: 0.85;
  }
  .food-card.urgency-warning {
    background: var(--sage-bg);
    border-color: var(--sage-lt);
  }

  .card-left {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    flex: 1;
    min-width: 0;
  }
  .card-emoji { font-size: 1.6rem; flex-shrink: 0; }
  .card-name {
    font-size: 1rem;
    font-weight: 800;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }
  .card-category {
    font-size: 0.74rem;
    background: #f0f0f0;
    border-radius: 20px;
    padding: 2px 10px;
    color: var(--text-mid);
    font-weight: 700;
    flex-shrink: 0;
  }
  .card-status {
    font-size: 0.88rem;
    font-weight: 700;
    color: var(--text-mid);
    white-space: nowrap;
    flex-shrink: 0;
  }

  .btn-delete {
    background: none;
    border: 1.5px solid #ddd;
    border-radius: var(--radius-sm);
    padding: 0.4rem 0.8rem;
    font-family: 'Nunito', sans-serif;
    font-size: 0.82rem;
    font-weight: 700;
    cursor: pointer;
    color: var(--text-mid);
    transition: all 0.15s;
    white-space: nowrap;
    flex-shrink: 0;
  }
  .btn-delete:hover {
    background: var(--red-lt);
    border-color: var(--red-border);
    color: #c0392b;
    transform: scale(1.04);
  }

  /* ── Empty state ──────────────────────────────────── */
  .empty-state {
    text-align: center;
    padding: 3.5rem 2rem;
    background: #f9f9f9;
    border: 2px dashed #d0d0d0;
    border-radius: 18px;
    color: #bbb;
  }
  .empty-icon { font-size: 3rem; margin-bottom: 0.8rem; }
  .empty-state strong { display: block; font-size: 1.05rem; color: var(--text-mid); margin-bottom: 0.4rem; }
  .empty-state span { font-size: 0.9rem; }

  /* ── Mascot ───────────────────────────────────────── */
  .mascot-box {
    display: flex;
    align-items: flex-start;
    gap: 1.2rem;
    border: 2px solid #e8e8e8;
    border-radius: 18px;
    padding: 1.5rem 1.8rem;
    margin-top: 2rem;
    background: var(--white);
    box-shadow: var(--shadow);
    transition: all 0.4s ease;
  }
  .mascot-face { font-size: 3.2rem; line-height: 1; flex-shrink: 0; }
  .mascot-msg {
    font-size: 1rem;
    font-weight: 700;
    line-height: 1.55;
    color: var(--text);
  }
  .mascot-tip {
    font-size: 0.84rem;
    color: var(--text-mid);
    font-style: italic;
    margin-top: 0.5rem;
    font-weight: 600;
  }

  /* ── Animations ───────────────────────────────────── */
  @keyframes fadeIn {
    from { opacity: 0; transform: translateY(-8px); }
    to   { opacity: 1; transform: translateY(0); }
  }
  @keyframes slideIn {
    from { opacity: 0; transform: translateX(-10px); }
    to   { opacity: 1; transform: translateX(0); }
  }
  @keyframes popIn {
    0%   { transform: scale(0.85); opacity: 0; }
    70%  { transform: scale(1.04); }
    100% { transform: scale(1); opacity: 1; }
  }

  /* ── Responsive ───────────────────────────────────── */
  @media (max-width: 768px) {
    .shell { grid-template-columns: 1fr; }
    .sidebar {
      position: static;
      height: auto;
      border-right: none;
      border-bottom: 2px solid var(--sage-lt);
    }
    .main { padding: 1.5rem 1rem 3rem; }
    .metrics { grid-template-columns: repeat(2, 1fr); }
    .page-header h1 { font-size: 2rem; }
  }
</style>
</head>
<body>

<div class="shell">

  <!-- ══════════════════ SIDEBAR ══════════════════ -->
  <aside class="sidebar">

    <div class="sidebar-logo">
      <h1>FridgeBuddy 🥕</h1>
      <p>your cozy fridge companion</p>
    </div>

    <hr />

    <div>
      <strong style="font-size:0.9rem; font-weight:800; display:block; margin-bottom:0.9rem;">➕ Add to Fridge</strong>

      <div style="margin-bottom:0.85rem;">
        <label class="form-label" for="food-name">Food Name</label>
        <input class="form-input" id="food-name" type="text" placeholder="e.g. Greek yogurt, Apples…" autocomplete="off" />
        <div class="emoji-preview" id="emoji-preview">start typing to see emoji ✨</div>
      </div>

      <div style="margin-bottom:0.85rem;">
        <label class="form-label" for="food-category">Category</label>
        <select class="form-select" id="food-category">
          <option value="Fruits">Fruits 🍎</option>
          <option value="Vegetables">Vegetables 🥦</option>
          <option value="Dairy">Dairy 🥛</option>
          <option value="Snacks">Snacks 🍪</option>
          <option value="Drinks">Drinks 🧃</option>
          <option value="Frozen">Frozen ❄️</option>
          <option value="Leftovers">Leftovers 🍱</option>
        </select>
      </div>

      <div style="margin-bottom:1rem;">
        <label class="form-label" for="food-expiry">Expiry Date</label>
        <input class="form-input" id="food-expiry" type="date" />
      </div>

      <button class="btn-add" onclick="handleAddFood()">🥗 Add to Fridge</button>

      <div class="toast" id="toast"></div>
    </div>

    <hr />

    <div class="sidebar-footer">
      Made with 💚 for college students<br />who forget about their food 😅
    </div>

  </aside>

  <!-- ══════════════════ MAIN ══════════════════ -->
  <main class="main">

    <div class="page-header">
      <h1>FridgeBuddy 🥕</h1>
      <p>your friendly fridge assistant — keeping your food (and your wallet) alive ✨</p>
    </div>

    <!-- Metrics -->
    <div class="metrics">
      <div class="metric-card">
        <div class="metric-label">📦 Total Items</div>
        <div class="metric-value" id="stat-total">0</div>
      </div>
      <div class="metric-card">
        <div class="metric-label">🔥 Expiring Soon</div>
        <div class="metric-value" id="stat-soon">0</div>
      </div>
      <div class="metric-card">
        <div class="metric-label">💀 Expired</div>
        <div class="metric-value" id="stat-expired">0</div>
      </div>
      <div class="metric-card">
        <div class="metric-label">♻️ Waste Prevented</div>
        <div class="metric-value" id="stat-waste">0</div>
      </div>
    </div>

    <!-- Expiring soon zone (conditionally shown) -->
    <div id="alert-zone" style="display:none;"></div>

    <!-- Food list -->
    <div class="section-title">🧊 Your Fridge</div>
    <div class="food-list" id="food-list"></div>

    <!-- Mascot -->
    <div class="mascot-box" id="mascot-box">
      <div class="mascot-face" id="mascot-face">😄</div>
      <div>
        <div class="mascot-msg" id="mascot-msg">Loading your fridge…</div>
        <div class="mascot-tip" id="mascot-tip"></div>
      </div>
    </div>

  </main>
</div>

<script>
// ════════════════════════════════════════════════════════
//  FOOD_UTILS — date math, urgency, emoji detection
// ════════════════════════════════════════════════════════

const EMOJI_MAP = {
  apple:'🍎', banana:'🍌', orange:'🍊', grape:'🍇', strawberr:'🍓',
  watermelon:'🍉', mango:'🥭', peach:'🍑', pear:'🍐', cherry:'🍒',
  lemon:'🍋', lime:'🍋', blueberr:'🫐', raspberr:'🍓', avocado:'🥑',
  pineapple:'🍍', coconut:'🥥', kiwi:'🥝',
  carrot:'🥕', broccoli:'🥦', spinach:'🥬', lettuce:'🥬', tomato:'🍅',
  cucumber:'🥒', pepper:'🫑', onion:'🧅', garlic:'🧄', potato:'🥔',
  corn:'🌽', mushroom:'🍄', celery:'🥬', cabbage:'🥬', zucchini:'🥒',
  milk:'🥛', cheese:'🧀', butter:'🧈', yogurt:'🫙', egg:'🥚', cream:'🥛',
  chicken:'🍗', beef:'🥩', pork:'🥓', fish:'🐟', salmon:'🐟',
  shrimp:'🍤', tuna:'🐟', meat:'🥩', bacon:'🥓', sausage:'🌭', tofu:'🫙',
  bread:'🍞', rice:'🍚', pasta:'🍝', noodle:'🍜', pizza:'🍕',
  burger:'🍔', sandwich:'🥪',
  cake:'🎂', cookie:'🍪', chocolate:'🍫', candy:'🍬', donut:'🍩',
  juice:'🧃', soda:'🥤', water:'💧', coffee:'☕', tea:'🍵',
  beer:'🍺', wine:'🍷',
  leftover:'🍱', soup:'🍲', salad:'🥗', sauce:'🫙', jam:'🫙',
  honey:'🍯', oil:'🫙', ice:'🍦',
};

const CATEGORY_EMOJI = {
  Fruits:'🍎', Vegetables:'🥦', Dairy:'🥛',
  Snacks:'🍪', Drinks:'🧃', Frozen:'❄️', Leftovers:'🍱',
};

function detectEmoji(name, category) {
  const lower = name.toLowerCase();
  for (const [key, emoji] of Object.entries(EMOJI_MAP)) {
    if (lower.includes(key)) return emoji;
  }
  return CATEGORY_EMOJI[category] || '🍽️';
}

function daysLeft(expiryDateStr) {
  try {
    const today = new Date(); today.setHours(0,0,0,0);
    const exp   = new Date(expiryDateStr + 'T00:00:00');
    return Math.round((exp - today) / 86400000);
  } catch { return null; }
}

function getUrgency(days) {
  if (days === null)  return 'ok';
  if (days < 0)       return 'expired';
  if (days <= 2)      return 'critical';
  if (days <= 5)      return 'warning';
  return 'ok';
}

function getStatusLabel(days) {
  if (days === null) return '⚠️ Unknown date';
  if (days < 0) return `💀 Expired ${Math.abs(days)} day${Math.abs(days)!==1?'s':''} ago`;
  if (days === 0) return '🔥 Expires TODAY';
  if (days === 1) return '⚡ Expires TOMORROW';
  if (days <= 2)  return `😬 Expires in ${days} days`;
  if (days <= 5)  return `🟡 ${days} days left`;
  if (days <= 14) return `🟢 ${days} days left`;
  return `✅ ${days} days left`;
}

function sortByExpiry(foods) {
  return [...foods].sort((a, b) => {
    const da = daysLeft(a.expiry_date);
    const db = daysLeft(b.expiry_date);
    return (da ?? 9999) - (db ?? 9999);
  });
}

function computeStats(foods) {
  const expiringSoon = foods.filter(f => getUrgency(daysLeft(f.expiry_date)) === 'critical');
  const expired      = foods.filter(f => getUrgency(daysLeft(f.expiry_date)) === 'expired');
  return {
    total: foods.length,
    expiringSoon,
    expired,
    wastePrevented: Math.max(0, foods.length - expired.length),
  };
}

// ════════════════════════════════════════════════════════
//  STORAGE — localStorage-backed JSON store
// ════════════════════════════════════════════════════════

const STORAGE_KEY = 'fridgebuddy_foods';

function loadFoods() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    return raw ? JSON.parse(raw) : [];
  } catch { return []; }
}

function saveFoods(foods) {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(foods));
}

function addFoodItem(name, category, emoji, expiryDate) {
  const foods = loadFoods();
  const item = {
    id: Date.now().toString(),
    name: name.trim(),
    category,
    emoji,
    expiry_date: expiryDate,
  };
  foods.push(item);
  saveFoods(foods);
  return item;
}

function deleteFoodItem(id) {
  const foods = loadFoods().filter(f => f.id !== id);
  saveFoods(foods);
}

// ════════════════════════════════════════════════════════
//  MASCOT MESSAGES
// ════════════════════════════════════════════════════════

const HEALTHY_MSGS = [
  "Your fridge is absolutely thriving ✨ no food casualties detected 🫡",
  "All items are safe and sound! I'm so proud of you 🥹",
  "Chef's kiss 🤌 — your fridge is living its best life right now.",
  "Zero drama in the fridge today. Seriously impressive fridge management. 💅",
  "Everything is fresh and fine. You deserve a gold star ⭐ — take two.",
];

const EXPIRING_MSGS = [
  (n,e) => `Girl PLEASE eat the ${n} ${e} — it's fighting for its life out there 😭`,
  (n,e) => `The ${n} ${e} is sending you a distress signal. It deserves better!! 🚨`,
  (n,e) => `POV: your ${n} ${e} at 2am wondering why you haven't eaten it yet 🫠`,
  (n,e) => `BREAKING: ${n} ${e} is on its last legs. This is not a drill. 😤`,
  (n,e) => `${n} ${e} said 'I thought we were friends' 😔 eat it before it's too late!`,
];

const EXPIRED_MSGS = [
  (n,e) => `We lost the ${n} ${e} soldier 💔 it has seen things... may it rest in peace 🕯️`,
  (n,e) => `Moment of silence for the ${n} ${e} 😔 it deserved better. We all did.`,
  (n,e) => `The ${n} ${e} has left the chat 👋 please delete it and move forward.`,
  (n,e) => `RIP ${n} ${e} — gone but not forgotten. Mostly just... gone. 🪦`,
];

const CHAOS_MSGS = [
  "Your fridge is living in complete chaos rn 😭 but we love you anyway 💚",
  "Multiple items at risk! This is a Code Green emergency 🚨 (green like the situation, not the mold 😬)",
  "The fridge is screaming internally. Please. PLEASE eat something. 🥺",
];

const TIPS = {
  empty:   "💡 Tip: Add your first item! Dairy & produce expire fastest — start there.",
  chaos:   "💡 Tip: Batch-cook everything expiring into one meal. Stir-fry saves lives.",
  expired: "💡 Tip: Hit 🗑️ to remove expired items and keep your tracker accurate.",
  warning: "💡 Tip: Items expiring within 2 days make great stir-fry, smoothies, or omelettes!",
  healthy: "💡 Tip: Keep adding items as you shop so FridgeBuddy can watch over your whole fridge!",
};

function pick(arr) { return arr[Math.floor(Math.random() * arr.length)]; }

function getMascotData(stats) {
  const { expiringSoon, expired, total } = stats;
  if (total === 0) return { msg: "Hey! Add your first item so I can keep watch 👀 I'm very responsible, I promise.", mood:'happy', tip: TIPS.empty };
  if (expiringSoon.length >= 3 && expired.length >= 1) return { msg: pick(CHAOS_MSGS), mood:'chaos', tip: TIPS.chaos };
  if (expired.length) {
    const f = expired[0];
    return { msg: pick(EXPIRED_MSGS)(f.name, f.emoji), mood:'sad', tip: TIPS.expired };
  }
  if (expiringSoon.length) {
    const f = expiringSoon[0];
    return { msg: pick(EXPIRING_MSGS)(f.name, f.emoji), mood:'worried', tip: TIPS.warning };
  }
  return { msg: pick(HEALTHY_MSGS), mood:'happy', tip: TIPS.healthy };
}

const MOOD_EMOJI = { happy:'😄', worried:'😰', sad:'😢', chaos:'🤯' };
const MOOD_COLORS = {
  happy:   { bg:'#f0f7f0', border:'#8fbc8f' },
  worried: { bg:'#fff8e1', border:'#ffd97d' },
  sad:     { bg:'#ffeaea', border:'#ff8a80' },
  chaos:   { bg:'#ffe8e3', border:'#ffb4a2' },
};

// ════════════════════════════════════════════════════════
//  UI RENDERING
// ════════════════════════════════════════════════════════

function renderAll() {
  const foods = loadFoods();
  const sorted = sortByExpiry(foods);
  const stats  = computeStats(foods);

  // Metrics
  document.getElementById('stat-total').textContent   = stats.total;
  document.getElementById('stat-soon').textContent    = stats.expiringSoon.length;
  document.getElementById('stat-expired').textContent = stats.expired.length;
  document.getElementById('stat-waste').textContent   = stats.wastePrevented;

  // Alert zone
  const alertZone = document.getElementById('alert-zone');
  const criticals = sorted.filter(f => getUrgency(daysLeft(f.expiry_date)) === 'critical');
  if (criticals.length) {
    alertZone.style.display = 'block';
    alertZone.innerHTML = `
      <div class="alert-zone">
        <div class="alert-zone-title">🚨 Eat These NOW — Expiring Within 2 Days!</div>
        ${criticals.map(f => `
          <div class="alert-item">
            <span style="font-size:1.3rem">${f.emoji}</span>
            <span>${f.name}</span>
            <span style="font-size:0.85rem; color:#9a6f00;">— ${getStatusLabel(daysLeft(f.expiry_date))}</span>
          </div>
        `).join('')}
      </div>`;
  } else {
    alertZone.style.display = 'none';
    alertZone.innerHTML = '';
  }

  // Food list
  const list = document.getElementById('food-list');
  if (sorted.length === 0) {
    list.innerHTML = `
      <div class="empty-state">
        <div class="empty-icon">🫙</div>
        <strong>Your fridge is empty!</strong>
        <span>Add your first item using the sidebar →</span>
      </div>`;
  } else {
    list.innerHTML = sorted.map(item => {
      const days    = daysLeft(item.expiry_date);
      const urgency = getUrgency(days);
      const status  = getStatusLabel(days);
      const catLabel = item.category || '';
      return `
        <div class="food-card urgency-${urgency}" id="card-${item.id}">
          <div class="card-left">
            <span class="card-emoji">${item.emoji}</span>
            <span class="card-name">${escHtml(item.name)}</span>
            <span class="card-category">${escHtml(catLabel)}</span>
          </div>
          <span class="card-status">${status}</span>
          <button class="btn-delete" onclick="handleDelete('${item.id}')">🗑️ Eat/Delete</button>
        </div>`;
    }).join('');
  }

  // Mascot
  const mascot = getMascotData(stats);
  const colors = MOOD_COLORS[mascot.mood] || MOOD_COLORS.happy;
  const box = document.getElementById('mascot-box');
  box.style.background = colors.bg;
  box.style.borderColor = colors.border;
  document.getElementById('mascot-face').textContent = MOOD_EMOJI[mascot.mood] || '🥕';
  document.getElementById('mascot-msg').textContent  = mascot.msg;
  document.getElementById('mascot-tip').textContent  = mascot.tip;
}

function escHtml(str) {
  return str.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
}

// ════════════════════════════════════════════════════════
//  EVENT HANDLERS
// ════════════════════════════════════════════════════════

function handleAddFood() {
  const name     = document.getElementById('food-name').value.trim();
  const category = document.getElementById('food-category').value;
  const expiry   = document.getElementById('food-expiry').value;
  const toast    = document.getElementById('toast');

  if (!name) {
    showToast('Please enter a food name! 🙈', 'error');
    return;
  }
  if (!expiry) {
    showToast('Please pick an expiry date! 📅', 'error');
    return;
  }

  const emoji = detectEmoji(name, category);
  addFoodItem(name, category, emoji, expiry);
  showToast(`Added ${emoji} ${name} to your fridge!`, 'success');

  document.getElementById('food-name').value = '';
  document.getElementById('emoji-preview').textContent = 'start typing to see emoji ✨';
  renderAll();
}

function handleDelete(id) {
  deleteFoodItem(id);
  renderAll();
}

function showToast(msg, type) {
  const toast = document.getElementById('toast');
  toast.textContent = msg;
  toast.className = `toast ${type}`;
  clearTimeout(toast._timer);
  toast._timer = setTimeout(() => { toast.className = 'toast'; }, 3000);
}

// ── Live emoji preview ──────────────────────────────────
document.getElementById('food-name').addEventListener('input', function() {
  const preview = document.getElementById('emoji-preview');
  const cat = document.getElementById('food-category').value;
  if (this.value.trim()) {
    const emoji = detectEmoji(this.value, cat);
    preview.textContent = `Detected emoji: ${emoji}`;
  } else {
    preview.textContent = 'start typing to see emoji ✨';
  }
});

// Allow Enter key to add food
document.getElementById('food-name').addEventListener('keydown', function(e) {
  if (e.key === 'Enter') handleAddFood();
});

// ── Set date default to today ───────────────────────────
(function() {
  const today = new Date();
  const yyyy = today.getFullYear();
  const mm   = String(today.getMonth() + 1).padStart(2, '0');
  const dd   = String(today.getDate()).padStart(2, '0');
  document.getElementById('food-expiry').value = `${yyyy}-${mm}-${dd}`;
})();

// ── Initial render ──────────────────────────────────────
renderAll();
</script>

</body>
</html>
