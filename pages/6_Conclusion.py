import streamlit as st
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.styling import apply_custom_style, apply_page_accent

st.set_page_config(page_title="Conclusion", page_icon="🏁", layout="wide")

apply_custom_style()
apply_page_accent("#6A1B9A")

st.title("🏁 Conclusion")
st.caption("Key insights, recommendations, and honest limitations from the Cricbuzz LiveStats project.")

st.divider()

# ---------------- Project recap metrics ----------------
c1, c2, c3, c4 = st.columns(4)
with c1:
    st.metric("SQL Queries", "25")
with c2:
    st.metric("Dashboard Pages", "6")
with c3:
    st.metric("Database Tables", "8")
with c4:
    st.metric("Data Sources", "API + MySQL")

st.divider()

# ============================================================
# KEY INSIGHTS
# ============================================================
st.header("💡 Key Insights")

insights = [
    ("🏏", "Standout All-Rounder",
     "Arjun Mehta: 2,508 ODI runs & 148 wickets across 36 matches — "
     "comfortably clears the >1000 runs / >50 wickets bar (Q9)."),
    ("🪙", "Toss ≠ Guaranteed Edge",
     "Win rate by toss decision (bat vs bowl first) sits close to a "
     "coin-flip in this dataset (Q17) — toss looks more venue/format "
     "dependent than a blanket advantage."),
    ("🇮🇳", "Most-Played Rivalry",
     "India vs Australia: 14 matches in the last 3 years (Q22) — the "
     "largest, most reliable sample of any head-to-head pair."),
    ("🎯", "Bowling Concentration",
     "Economy-rate leaders (Q18) cluster around just 2 bowlers — "
     "consistent with how real limited-overs attacks lean on a few "
     "specialists rather than spreading evenly."),
]

for i in range(0, len(insights), 2):
    cols = st.columns(2)
    for col, (icon, title, body) in zip(cols, insights[i:i+2]):
        with col:
            with st.container(border=True):
                st.markdown(f"**{icon} {title}**")
                st.caption(body)

st.divider()

# ============================================================
# BUSINESS RECOMMENDATIONS
# ============================================================
st.header("📌 Business Recommendations")

recommendations = [
    ("🧩", "Prioritize All-Rounders in Squad Building",
     "Since versatile players (Q9) can clear both batting and bowling "
     "volume thresholds when given a settled XI spot, selectors building "
     "white-ball squads should specifically scout and retain genuine "
     "all-rounders rather than treating batting and bowling depth as "
     "separate hiring problems."),
    ("⚖️", "Don't Over-Weight Toss in Predictions",
     "Q17's near-coin-flip result suggests prediction models and pre-match "
     "punditry should assign toss outcome a smaller weight than commonly "
     "assumed — venue and squad form are likely stronger signals."),
    ("📊", "Flag Low-Sample Rivalries as Less Reliable",
     "Only team pairs with a genuinely large head-to-head sample (like "
     "India vs Australia at 14 matches, Q22) should be used for confident "
     "head-to-head narratives — smaller samples deserve a caveat, not a "
     "headline stat."),
    ("🎯", "Scout and Retain Death-Overs Specialists",
     "Because economical bowling concentrates among a handful of players "
     "(Q18), team management should treat elite death-overs economy as a "
     "scarce, high-value skill worth specifically retaining — not assume "
     "it's evenly replaceable across the squad."),
    ("🗃️", "Expand to Real Historical Data Over Time",
     "The advanced trend queries (Q19, Q25) are currently proven on "
     "engineered data — the natural next step is feeding in real "
     "multi-season historical records so consistency and career-trajectory "
     "analysis reflects genuine (messier) player careers."),
]

for i in range(0, len(recommendations), 2):
    cols = st.columns(2)
    for col, (icon, title, body) in zip(cols, recommendations[i:i+2]):
        with col:
            with st.container(border=True):
                st.markdown(f"**{icon} {title}**")
                st.caption(body)

st.divider()

# ============================================================
# ASSUMPTIONS & LIMITATIONS
# ============================================================
st.header("⚠️ Assumptions & Limitations")

assumptions_limitations = [
    ("🧩", "Team = Country Assumption",
     "A player's 'team' for home/away (Q12) and close-match (Q15) logic "
     "is inferred from matching player country to team country — doesn't "
     "hold for franchise/domestic cricket."),
    ("🌍", "No Neutral-Venue Handling",
     "Home/away (Q12) compares venue country to team country only — "
     "doesn't account for tournaments hosted in a third country."),
    ("🧪", "Synthetic Seed Data",
     "Seed data was engineered so all 25 queries clear their thresholds "
     "(e.g. ≥20 matches, ≥6 quarters) — real data would likely be sparser "
     "and messier for advanced queries like Q19 and Q25."),
    ("🔌", "API Freshness Capped",
     "RapidAPI's free tier (200 requests/month) means Live Match / Top "
     "Player Stats reflect the last cached fetch, not guaranteed "
     "real-time data."),
    ("☁️", "Shared Free-Tier Database",
     "The Aiven MySQL instance is a free-tier service also hosting a "
     "separate project — storage/connection limits are shared."),
]

for i in range(0, len(assumptions_limitations), 2):
    cols = st.columns(2)
    for col, (icon, title, body) in zip(cols, assumptions_limitations[i:i+2]):
        with col:
            with st.container(border=True):
                st.markdown(f"**{icon} {title}**")
                st.caption(body)

st.divider()

# ============================================================
# CLOSING / THANK YOU
# ============================================================
st.markdown("""
<div style="text-align:center; padding: 2rem 1rem;">
    <h2>🙏 Thank You</h2>
    <p style="font-size:1.05rem; opacity:0.85; max-width:700px; margin:0 auto;">
        Thanks for exploring Cricbuzz LiveStats — a project built to bring
        live cricket data, SQL analytics, and hands-on database management
        together in one dashboard. Feedback and suggestions are always welcome.
    </p>
</div>
""", unsafe_allow_html=True)

col_a, col_b, col_c = st.columns([1, 1, 1])
with col_b:
    if st.button("🎉 Celebrate", use_container_width=True):
        st.balloons()

st.caption("Built as part of the Cricbuzz LiveStats project.")
