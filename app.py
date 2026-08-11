
import math
import string
import time
from itertools import product

import streamlit as st

st.set_page_config(
    page_title="Password Lab 🔐",
    page_icon="🔐",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# -----------------------------
# Styling
# -----------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Space+Mono:wght@400;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}
.stApp {
    background:
      radial-gradient(circle at 15% 10%, rgba(55, 65, 81, .35), transparent 28%),
      radial-gradient(circle at 85% 15%, rgba(37, 99, 235, .18), transparent 30%),
      #080b12;
}
.block-container {
    max-width: 1200px;
    padding-top: 2rem;
    padding-bottom: 2rem;
}
.hero {
    padding: 1.4rem 1.6rem 1.2rem;
    border: 1px solid rgba(148,163,184,.22);
    border-radius: 24px;
    background: linear-gradient(135deg, rgba(15,23,42,.94), rgba(17,24,39,.72));
    box-shadow: 0 20px 60px rgba(0,0,0,.28);
}
.kicker {
    font-family: 'Space Mono', monospace;
    letter-spacing: .12em;
    font-size: .78rem;
    opacity: .7;
    text-transform: uppercase;
}
.hero h1 {
    font-size: clamp(2.1rem, 5vw, 4rem);
    margin: .15rem 0 .1rem;
    font-weight: 800;
}
.hero p {
    margin: 0;
    color: #cbd5e1;
    font-size: 1.05rem;
}
.card {
    border: 1px solid rgba(148,163,184,.18);
    border-radius: 18px;
    padding: 1rem 1.1rem;
    background: rgba(15,23,42,.72);
    height: 100%;
}
.card h3 {
    margin-top: 0;
}
.mono {
    font-family: 'Space Mono', monospace;
}
.big {
    font-size: 1.55rem;
    font-weight: 800;
}
.verdict {
    border-radius: 18px;
    padding: 1.2rem;
    text-align: center;
    border: 1px solid rgba(255,255,255,.14);
    background: rgba(15,23,42,.85);
}
.verdict .emoji {
    font-size: 3rem;
}
.verdict .title {
    font-size: 1.35rem;
    font-weight: 800;
    margin-top: .2rem;
}
.verdict .sub {
    color: #cbd5e1;
    margin-top: .35rem;
}
.guessbox {
    font-family: 'Space Mono', monospace;
    padding: .85rem 1rem;
    border-radius: 12px;
    background: #020617;
    border: 1px solid rgba(96,165,250,.25);
    color: #93c5fd;
    min-height: 2.8rem;
}
.footer {
    text-align:center;
    color:#94a3b8;
    font-size:.85rem;
    padding:1.5rem 0 .5rem;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# Safe educational analysis
# -----------------------------
def character_pool(password):
    pool = 0
    if any(c.islower() for c in password): pool += 26
    if any(c.isupper() for c in password): pool += 26
    if any(c.isdigit() for c in password): pool += 10
    if any(c in string.punctuation for c in password): pool += len(string.punctuation)
    return pool

def search_space(password):
    pool = character_pool(password)
    if not password or pool == 0:
        return 0, 0
    log10 = len(password) * math.log10(pool)
    return pool, log10

def common_pattern(password):
    p = password.lower()
    common = [
        "password", "qwerty", "admin", "welcome", "letmein",
        "123456", "12345678", "abc123", "pass123"
    ]
    if p in common or any(x in p for x in common):
        return True, "A very common password pattern"
    if p.isdigit():
        return True, "Only numbers"
    if p.isalpha() and p.islower():
        return True, "Only lowercase letters"
    if len(set(p)) <= max(2, len(p)//3):
        return True, "Lots of repeated characters"
    return False, ""

def analyse(password):
    length = len(password)
    lower = any(c.islower() for c in password)
    upper = any(c.isupper() for c in password)
    digit = any(c.isdigit() for c in password)
    symbol = any(c in string.punctuation for c in password)
    pattern, reason = common_pattern(password)
    pool, log10 = search_space(password)

    # Educational score; not a real-world password-cracking estimate.
    score = 0
    score += min(length * 4, 48)
    score += 10 if lower else 0
    score += 10 if upper else 0
    score += 10 if digit else 0
    score += 12 if symbol else 0
    score -= 20 if pattern else 0
    score = max(0, min(100, score))

    if score < 30:
        level, emoji = "VERY WEAK", "🔴"
    elif score < 55:
        level, emoji = "WEAK", "🟠"
    elif score < 75:
        level, emoji = "MODERATE", "🟡"
    else:
        level, emoji = "STRONGER", "🟢"

    return {
        "length": length, "lower": lower, "upper": upper, "digit": digit,
        "symbol": symbol, "pattern": pattern, "reason": reason,
        "pool": pool, "log10": log10, "score": score,
        "level": level, "emoji": emoji
    }

def human_search_space(log10):
    if log10 == 0:
        return "—"
    if log10 < 3:
        return f"≈ {10**log10:,.0f}"
    exponent = int(math.floor(log10))
    mantissa = 10 ** (log10 - exponent)
    return f"≈ {mantissa:.2f} × 10^{exponent}"

def educational_guess_demo(target, max_length=4):
    """
    A deliberately tiny, local demonstration only.
    It never connects to accounts, websites, login forms, or networks.
    For longer targets the UI shows the mathematical search-space estimate
    instead of performing an exhaustive search.
    """
    alphabet = string.ascii_lowercase + string.digits
    if len(target) > max_length or any(c not in alphabet for c in target.lower()):
        return None, 0, "large"
    target = target.lower()
    attempts = 0
    for length in range(1, len(target) + 1):
        for chars in product(alphabet, repeat=length):
            guess = ''.join(chars)
            attempts += 1
            if guess == target:
                return guess, attempts, "found"
    return None, attempts, "not_found"

# -----------------------------
# UI
# -----------------------------
st.markdown("""
<div class="hero">
  <div class="kicker">CYBERSECURITY • EDUCATIONAL SIMULATOR</div>
  <h1>🔐 PASSWORD LAB</h1>
  <p>How predictable is a password? Let's put the mathematics under the microscope.</p>
</div>
""", unsafe_allow_html=True)

st.warning("⚠️ Use only a fictional test password. Never enter a real password or anything used for an actual account.")

if "last_password" not in st.session_state:
    st.session_state.last_password = ""
if "analysis" not in st.session_state:
    st.session_state.analysis = None
if "simulate" not in st.session_state:
    st.session_state.simulate = False
if "show_why" not in st.session_state:
    st.session_state.show_why = False

st.write("")
password = st.text_input(
    "DROP YOUR TEST PASSWORD HERE",
    type="password",
    placeholder="Try something fictional, e.g. cat123",
    help="This value stays inside this app session and is used only for the local educational simulation."
)

c1, c2, c3 = st.columns([1.2, 1.2, 1])
with c1:
    analyse_btn = st.button("🧠 LET'S DISSECT IT", use_container_width=True)
with c2:
    simulate_btn = st.button("⚡ CRACK THE SIMULATION", use_container_width=True)
with c3:
    compare_btn = st.button("🥊 PASSWORD BATTLE", use_container_width=True)

if analyse_btn or simulate_btn:
    if not password:
        st.error("Give the lab a fictional password first.")
    else:
        st.session_state.last_password = password
        st.session_state.analysis = analyse(password)
        st.session_state.simulate = simulate_btn
        st.session_state.show_why = False

a = st.session_state.analysis
if a:
    st.write("")
    left, right = st.columns([1, 1.25], gap="large")

    with left:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### 🧠 LET'S DISSECT IT")
        st.metric("Length", f"{a['length']} characters")
        cols = st.columns(2)
        checks = [
            ("Lowercase", a["lower"]),
            ("Uppercase", a["upper"]),
            ("Numbers", a["digit"]),
            ("Symbols", a["symbol"]),
        ]
        for i, (name, yes) in enumerate(checks):
            cols[i % 2].write(f"**{name}**  {'✓' if yes else '—'}")
        st.write("")
        st.write("**GUESSING SPACE**")
        st.progress(min(a["score"]/100, 1.0))
        st.markdown(f'<div class="mono">{human_search_space(a["log10"])} possible combinations (theoretical)</div>', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        st.write("")
        st.markdown(f"""
        <div class="verdict">
          <div class="emoji">{a["emoji"]}</div>
          <div class="title">{a["level"]}</div>
          <div class="sub">This is an educational score — not a guarantee of real-world security.</div>
        </div>
        """, unsafe_allow_html=True)

    with right:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### ⚡ THE SIMULATION")
        if st.session_state.simulate:
            if a["length"] <= 4 and all(ch.lower() in string.ascii_lowercase + string.digits for ch in password):
                st.info("Tiny demonstration mode: searching a deliberately limited toy alphabet locally.")
                placeholder = st.empty()
                progress = st.progress(0)
                result, attempts, status = educational_guess_demo(password)
                total_estimate = max(1, (36 ** len(password)))
                # Show a short, dramatic animation without running the exhaustive loop repeatedly.
                for pct in [0.12, 0.28, 0.45, 0.63, 0.82, 1.0]:
                    progress.progress(pct)
                    placeholder.markdown(f'<div class="guessbox">SEARCHING...  {int(pct*100):02d}%</div>', unsafe_allow_html=True)
                    time.sleep(0.08)
                placeholder.markdown(f'<div class="guessbox">✓ MATCH FOUND — {attempts:,} toy attempts</div>', unsafe_allow_html=True)
                st.success("🔓 The fictional test password was found inside the tiny demonstration space.")
            else:
                st.warning("🛡️ NICE TRY. The search space is too large for an exhaustive demo.")
                st.metric("Theoretical possibilities", human_search_space(a["log10"]))
                st.caption("Instead of pretending to run billions or trillions of guesses, the lab stops and shows the mathematics. That's the point of the experiment.")
        else:
            st.markdown("""
            <div style="padding:1.2rem 0;color:#cbd5e1;">
            Press <b>⚡ CRACK THE SIMULATION</b> to start the safe, local demonstration.
            </div>
            """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    st.write("")
    b1, b2 = st.columns([1, 1])
    with b1:
        if st.button("💀 SHOW ME THE DAMAGE", use_container_width=True):
            st.session_state.show_why = True
    with b2:
        if st.button("🛡️ HOW DO I MAKE IT BETTER?", use_container_width=True):
            st.session_state.show_why = "tips"

    if st.session_state.show_why is True:
        st.info(
            "Why this score? "
            + (a["reason"] + ". " if a["pattern"] else "")
            + f"The password is {a['length']} characters long and uses "
            + str(sum([a["lower"], a["upper"], a["digit"], a["symbol"]]))
            + " character categories. Longer, less predictable passwords generally create a much larger search space."
        )
    elif st.session_state.show_why == "tips":
        st.success("🛡️ Aim for a long, unique password/passphrase, avoid obvious personal information, don't reuse important passwords, and turn on multi-factor authentication.")

# Password battle
if compare_btn:
    st.session_state.compare = True

if st.session_state.get("compare", False):
    st.write("")
    st.markdown("## 🥊 PASSWORD BATTLE")
    st.caption("Use two fictional examples only.")
    p1, p2 = st.columns(2)
    with p1:
        pw_a = st.text_input("PASSWORD A", type="password", key="pw_a", placeholder="e.g. cat123")
    with p2:
        pw_b = st.text_input("PASSWORD B", type="password", key="pw_b", placeholder="e.g. BlueTiger42")
    if pw_a and pw_b:
        aa, bb = analyse(pw_a), analyse(pw_b)
        cols = st.columns(2)
        for col, label, x in [(cols[0], "A", aa), (cols[1], "B", bb)]:
            with col:
                st.markdown(f"### {label} {x['emoji']} {x['level']}")
                st.metric("Length", x["length"])
                st.metric("Theoretical search space", human_search_space(x["log10"]))
                st.progress(x["score"]/100)
        if aa["score"] > bb["score"]:
            st.info("🏆 In this educational scoring model, PASSWORD A scores higher.")
        elif bb["score"] > aa["score"]:
            st.info("🏆 In this educational scoring model, PASSWORD B scores higher.")
        else:
            st.info("🤝 They score the same in this simplified model.")

st.markdown("""
<div class="footer">
  PASSWORD LAB • A safe demonstration of search spaces, string analysis and security thinking.<br>
  No accounts are contacted. No login forms are attacked. No real passwords should be entered.
</div>
""", unsafe_allow_html=True)
