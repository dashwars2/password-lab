import math, string, time
from itertools import product
import streamlit as st

st.set_page_config(page_title="PASSWORD LAB // Cybersecurity Simulator", page_icon="🔐", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&family=Space+Mono:wght@400;700&display=swap');
body{background:#02040a}
.stApp{
  background:
    repeating-linear-gradient(
      0deg,
      rgba(0,220,255,.10) 0px,
      rgba(0,220,255,.10) 1px,
      transparent 1px,
      transparent 45px
    ),
    repeating-linear-gradient(
      90deg,
      rgba(0,220,255,.10) 0px,
      rgba(0,220,255,.10) 1px,
      transparent 1px,
      transparent 45px
    ),
    repeating-linear-gradient(
      0deg,
      rgba(168,85,247,.035) 0px,
      rgba(168,85,247,.035) 1px,
      transparent 1px,
      transparent 15px
    ),
    repeating-linear-gradient(
      90deg,
      rgba(168,85,247,.035) 0px,
      rgba(168,85,247,.035) 1px,
      transparent 1px,
      transparent 15px
    ),
    radial-gradient(circle at 10% 15%,rgba(0,220,255,.22),transparent 28%),
    radial-gradient(circle at 90% 20%,rgba(0,255,140,.16),transparent 25%),
    radial-gradient(circle at 50% 85%,rgba(150,50,255,.18),transparent 30%),
    #02060d;
  color:#e5edf8;
  background-attachment:fixed;
}
.block-container{max-width:1250px;padding:2rem}
*{font-family:Inter,sans-serif}
.hero{border:1px solid #00d9ff;border-radius:24px;padding:28px 30px;background:rgba(3,10,20,.90);box-shadow:0 0 25px rgba(0,217,255,.12),inset 0 0 30px rgba(0,217,255,.04)}
.badge{font:700 11px 'Space Mono';letter-spacing:.16em;color:#7dd3fc}
.hero h1{font-size:clamp(42px,6vw,76px);line-height:.92;margin:10px 0;font-weight:800;letter-spacing:-.06em}
.hero p{color:#a8b8cc;font-size:16px;max-width:780px}
.status{float:right;padding:7px 12px;border:1px solid #14532d;color:#86efac;background:#052e16;border-radius:999px;font:700 10px 'Space Mono'}

.hero-strip{display:flex;gap:8px;flex-wrap:wrap;margin-top:18px}
.hero-strip span{font:700 9px "Space Mono";letter-spacing:.08em;color:#7dd3fc;padding:6px 9px;border:1px solid #16445c;border-radius:999px;background:rgba(2,12,22,.6)}
.quick-card{border:1px solid #16344b;background:rgba(5,12,22,.82);border-radius:14px;padding:13px 14px;height:100%}
.quick-card .qtitle{font:700 10px "Space Mono";color:#6d829a;letter-spacing:.08em;text-transform:uppercase}
.quick-card .qvalue{font-size:18px;font-weight:800;margin-top:5px}
.quick-card .qsub{font-size:11px;color:#8194aa;margin-top:3px}
.demo-chip{font:700 10px "Space Mono";color:#8be7ff}
.section{font:700 11px 'Space Mono';letter-spacing:.13em;color:#64748b;margin:24px 0 8px}
.panel{border:1px solid #16445c;background:rgba(5,12,22,.90);border-radius:18px;padding:20px;box-shadow:0 0 18px rgba(0,190,255,.04),inset 0 0 28px rgba(0,180,255,.03)}
.metric{border:1px solid #1c2a3d;background:#080e19;border-radius:14px;padding:14px;min-height:76px}
.metric .label{font:600 10px 'Space Mono';color:#71839a}
.metric .value{font-size:21px;font-weight:800;margin-top:7px}
.verdict{text-align:center;border:1px solid #26364c;border-radius:18px;padding:18px;background:#0b1220}
.verdict .emoji{font-size:42px}.verdict .title{font-size:22px;font-weight:800}.verdict .sub{color:#8fa2bb;font-size:12px}
.terminal{background:#03060b;border:1px solid #1d3044;border-radius:16px;padding:16px;font:14px 'Space Mono';color:#9bd7ff;min-height:150px}
.big{font:800 30px 'Space Mono';color:#dbeafe}
.tip{padding:12px 14px;border-left:3px solid #38bdf8;background:#08121e;border-radius:8px;margin:7px 0;color:#b7c6d8}
.footer{text-align:center;color:#52657b;font:10px 'Space Mono';padding:25px}
div.stButton>button{border-radius:12px!important;border:1px solid #26384f!important;background:#0b1422!important;color:#e5edf8!important;font-weight:700!important;min-height:46px}
div.stButton>button:hover{border-color:#38bdf8!important;color:#7dd3fc!important}
[data-testid="stTextInput"] input{background:#050a12!important;border:1px solid #26384f!important;border-radius:12px!important;color:#e5edf8!important}

.feature-grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:12px;margin-top:8px}
.feature-card{border:1px solid #21415a;background:linear-gradient(180deg,rgba(7,18,32,.94),rgba(5,12,22,.88));border-radius:16px;padding:16px;min-height:128px;box-shadow:inset 0 0 20px rgba(0,210,255,.025),0 8px 24px rgba(0,0,0,.18)}
.feature-card:hover{border-color:#22d3ee}
.feature-icon{font-size:25px}
.feature-title{font:800 13px Inter,sans-serif;margin-top:8px}
.feature-sub{font-size:11px;color:#8ca0b7;line-height:1.45;margin-top:5px}
.dash-head{display:flex;justify-content:space-between;align-items:end;gap:16px}
.dash-label{font:700 10px "Space Mono";letter-spacing:.13em;color:#6d829a}
.dash-title{font-size:22px;font-weight:800;margin-top:3px}
.kpi-row{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:10px;margin-top:14px}
.kpi{border:1px solid #1c3348;background:rgba(5,13,23,.9);border-radius:14px;padding:12px}
.kpi .klabel{font:700 9px "Space Mono";color:#6d829a;letter-spacing:.08em}
.kpi .kvalue{font-size:18px;font-weight:800;margin-top:6px}
@media(max-width:900px){.feature-grid{grid-template-columns:repeat(2,minmax(0,1fr))}.kpi-row{grid-template-columns:repeat(2,minmax(0,1fr))}}
</style>
""", unsafe_allow_html=True)

def pool(p):
    return (26 if any(c.islower() for c in p) else 0)+(26 if any(c.isupper() for c in p) else 0)+(10 if any(c.isdigit() for c in p) else 0)+(len(string.punctuation) if any(c in string.punctuation for c in p) else 0)

def space(p):
    q=pool(p)
    return (q, len(p)*math.log10(q) if p and q else 0)

def analyse(p):
    lo=any(c.islower() for c in p); up=any(c.isupper() for c in p); di=any(c.isdigit() for c in p); sy=any(c in string.punctuation for c in p)
    common=["password","qwerty","admin","welcome","123456","abc123"]
    pattern=(p.lower() in common or any(x in p.lower() for x in common) or p.isdigit() or (p.isalpha() and p.islower()))
    reason="common/predictable pattern" if pattern else ""
    q,lg=space(p)
    score=max(0,min(100,min(len(p)*4,48)+(10 if lo else 0)+(10 if up else 0)+(10 if di else 0)+(12 if sy else 0)-(20 if pattern else 0)))
    level,emoji=("VERY WEAK","🔴") if score<30 else ("WEAK","🟠") if score<55 else ("MODERATE","🟡") if score<75 else ("STRONGER","🟢")
    return dict(length=len(p),lo=lo,up=up,di=di,sy=sy,pattern=pattern,reason=reason,q=q,lg=lg,score=score,level=level,emoji=emoji)

def hs(lg):
    if not lg:return "—"
    if lg<3:return f"{10**lg:,.0f}"
    e=int(math.floor(lg)); return f"{10**(lg-e):.2f} × 10^{e}"

def toy_guess(target):
    alphabet=string.ascii_lowercase+string.digits
    if len(target)>4 or any(c.lower() not in alphabet for c in target): return 0
    target=target.lower(); n=0
    for L in range(1,len(target)+1):
        for chars in product(alphabet,repeat=L):
            n+=1
            if ''.join(chars)==target:return n
    return 0

if "a" not in st.session_state: st.session_state.a=None
if "sim" not in st.session_state: st.session_state.sim=False
if "battle" not in st.session_state: st.session_state.battle=False

st.markdown("""
<div class="hero">
  <span class="status">● SIMULATION ONLINE</span>
  <div class="badge">CS FAIR // CYBERSECURITY LAB</div>
  <h1>PASSWORD<br>LAB 🔐</h1>
  <p>Can a computer guess it? Explore the mathematics behind password security — safely, visually, and locally.</p>
  <div class="hero-strip">
    <span>LOCAL ONLY</span><span>NO ACCOUNTS</span><span>EDUCATIONAL MODE</span>
  </div>
</div>
""",unsafe_allow_html=True)

st.markdown('<div class="section">01 // ENTER A TEST PASSWORD</div>',unsafe_allow_html=True)
st.warning("⚠️ Fiction only. Never enter a real password, account password, or anything used to log in.")

p=st.text_input("Test password",type="password",placeholder="Type a fictional test password…",label_visibility="collapsed")

c1,c2,c3=st.columns(3)
with c1: ab=st.button("🧠  DISSECT IT",use_container_width=True)
with c2: sb=st.button("⚡  RUN SIMULATION",use_container_width=True)
with c3: bb=st.button("🥊  PASSWORD BATTLE",use_container_width=True)

st.markdown('<div style="height:10px"></div>',unsafe_allow_html=True)

st.markdown("""
<div class="dash-head">
  <div>
    <div class="dash-label">02 // LAB DASHBOARD</div>
    <div class="dash-title">Choose a tool. Run an experiment.</div>
  </div>
  <div class="demo-chip">● READY FOR DEMO</div>
</div>

<div class="feature-grid">
  <div class="feature-card">
    <div class="feature-icon">🧠</div>
    <div class="feature-title">DISSECT IT</div>
    <div class="feature-sub">Break down length, character variety and predictable patterns.</div>
  </div>
  <div class="feature-card">
    <div class="feature-icon">⚡</div>
    <div class="feature-title">RUN SIMULATION</div>
    <div class="feature-sub">Watch the safe local guessing demo and see the search space grow.</div>
  </div>
  <div class="feature-card">
    <div class="feature-icon">🥊</div>
    <div class="feature-title">PASSWORD BATTLE</div>
    <div class="feature-sub">Compare two fictional passwords side by side.</div>
  </div>
  <div class="feature-card">
    <div class="feature-icon">💀</div>
    <div class="feature-title">SHOW THE DAMAGE</div>
    <div class="feature-sub">See exactly why the lab scored a password the way it did.</div>
  </div>
</div>

<div class="kpi-row">
  <div class="kpi"><div class="klabel">MODE</div><div class="kvalue">LOCAL</div></div>
  <div class="kpi"><div class="klabel">NETWORK</div><div class="kvalue">OFFLINE</div></div>
  <div class="kpi"><div class="klabel">ACCOUNTS</div><div class="kvalue">NONE</div></div>
  <div class="kpi"><div class="klabel">PURPOSE</div><div class="kvalue">LEARN</div></div>
</div>
""", unsafe_allow_html=True)

if bb:
    st.session_state.battle=True


a=st.session_state.a
if p and not a:
    st.caption("TIP // Start with a short fictional example like `cat123`, then run DISSECT IT.")

if a:
    st.markdown('<div class="section">03 // THE AUTOPSY</div>',unsafe_allow_html=True)
    L,R=st.columns([1,1.15],gap="large")
    with L:
        st.markdown('<div class="panel">',unsafe_allow_html=True); st.markdown("### 🧠 LET'S DISSECT IT")
        cols=st.columns(3)
        for col,lab,val in zip(cols,["LENGTH","CHARACTER POOL","SEARCH SPACE"],[f"{a['length']} chars",a["q"],hs(a["lg"])]):
            col.markdown(f'<div class="metric"><div class="label">{lab}</div><div class="value">{val}</div></div>',unsafe_allow_html=True)
        st.write("")
        cols=st.columns(4)
        for col,(lab,v) in zip(cols,[("lowercase",a["lo"]),("uppercase",a["up"]),("numbers",a["di"]),("symbols",a["sy"])]):
            col.markdown(f'<div class="metric"><div class="label">{lab}</div><div class="value">{"✓" if v else "—"}</div></div>',unsafe_allow_html=True)
        st.write(""); st.markdown("**PREDICTABILITY CHECK**"); st.progress(a["score"]/100)
        st.caption("Educational score — not a real-world cracking-time guarantee.")
        st.markdown('</div>',unsafe_allow_html=True); st.write("")
        st.markdown(f'<div class="verdict"><div class="emoji">{a["emoji"]}</div><div class="title">{a["level"]}</div><div class="sub">A larger search space means more possibilities to explore.</div></div>',unsafe_allow_html=True)
    with R:
        st.markdown('<div class="panel">',unsafe_allow_html=True); st.markdown("### ⚡ THE GUESSING TERMINAL")
        box=st.empty()
        if st.session_state.sim:
            if len(p)<=4 and all(c.lower() in string.ascii_lowercase+string.digits for c in p):
                box.markdown('<div class="terminal">> booting educational simulator…<br>> target stored locally<br>> toy alphabet: a-z + 0-9<br>> searching…</div>',unsafe_allow_html=True)
                for pct in [15,35,55,75,100]:
                    time.sleep(.08); box.markdown(f'<div class="terminal">> search engine: ONLINE<br>> progress: {pct}%<br>> scanning candidate space…</div>',unsafe_allow_html=True)
                n=toy_guess(p); box.markdown(f'<div class="terminal">> <b>✓ MATCH FOUND</b><br>> toy attempts: {n:,}<br>> simulation complete.</div>',unsafe_allow_html=True)
            else:
                box.markdown(f'<div class="terminal">> <b>⚠ SEARCH SPACE TOO LARGE</b><br>> theoretical possibilities:<br><div class="big">{hs(a["lg"])}</div>> exhaustive demo halted<br>> mathematics mode: ACTIVE</div>',unsafe_allow_html=True)
        else:
            box.markdown('<div class="terminal">> waiting for command…<br>> press RUN SIMULATION<br>> no accounts • no networks • no login forms</div>',unsafe_allow_html=True)
        st.markdown('</div>',unsafe_allow_html=True)
    x,y=st.columns(2)
    with x:
        if st.button("💀  SHOW ME THE DAMAGE",use_container_width=True):
            st.info(f"**VERDICT LOG:** {a['reason']+'. ' if a['reason'] else ''}Length: {a['length']} characters. Character categories: {sum([a['lo'],a['up'],a['di'],a['sy']])}. Longer and less predictable passwords generally create a much larger search space.")
    with y:
        if st.button("🛡️  HOW DO I BEAT THIS?",use_container_width=True):
            st.success("🛡️ **DEFENCE MODE:** Use a long, unique password/passphrase. Avoid obvious personal information and reused passwords. Use a password manager where appropriate and enable multi-factor authentication.")

if st.session_state.battle:
    st.markdown('<div class="section">05 // PASSWORD BATTLE</div>',unsafe_allow_html=True)
    st.markdown('<div class="panel">',unsafe_allow_html=True); st.markdown("### 🥊 TWO PASSWORDS ENTER. ONE SEARCH SPACE WINS.")
    x,y=st.columns(2)
    with x: pa=st.text_input("PASSWORD A",type="password",key="pa",placeholder="fictional example")
    with y: pb=st.text_input("PASSWORD B",type="password",key="pb",placeholder="fictional example")
    if pa and pb:
        aa,bb=analyse(pa),analyse(pb)
        for col,lab,z in [(x,"A",aa),(y,"B",bb)]:
            with col:
                st.markdown(f"#### {lab} {z['emoji']} {z['level']}"); st.progress(z["score"]/100); st.write(f"**Length:** {z['length']} | **Search space:** {hs(z['lg'])}")
        st.success("🏆 "+("PASSWORD A scores higher." if aa["score"]>bb["score"] else "PASSWORD B scores higher." if bb["score"]>aa["score"] else "It's a tie.")+" This is a simplified educational model.")
    st.markdown('</div>',unsafe_allow_html=True)

st.markdown('<div class="section">04 // WHY THIS MATTERS</div>',unsafe_allow_html=True)
m1,m2,m3=st.columns(3)
for col,title,icon,text in [
    (m1,"SEARCH SPACE","📊","More possibilities can mean more work for a guessing algorithm."),
    (m2,"PREDICTABILITY","🧩","Common patterns can make passwords easier to guess."),
    (m3,"DEFENCE","🛡️","Long, unique passwords plus MFA make better protection.")
]:
    with col:
        st.markdown(f'<div class="quick-card"><div class="qtitle">{icon} {title}</div><div class="qsub" style="margin-top:8px;font-size:12px">{text}</div></div>',unsafe_allow_html=True)

st.markdown('<div class="section">04 // THE TAKEAWAY</div><div class="panel"><div class="tip">🔑 <b>LONGER</b> → more possible combinations</div><div class="tip">🧩 <b>LESS PREDICTABLE</b> → harder to guess</div><div class="tip">🛡️ <b>UNIQUE + MFA</b> → better account protection</div></div>',unsafe_allow_html=True)
st.markdown('<div class="footer">PASSWORD LAB // SAFE EDUCATIONAL SIMULATOR // NO ACCOUNTS CONTACTED // NO REAL PASSWORDS</div>',unsafe_allow_html=True)
