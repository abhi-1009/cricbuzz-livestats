import streamlit as st
from utils.styling import apply_custom_style, apply_page_accent

st.set_page_config(
    page_title="Cricbuzz LiveStats",
    page_icon= "🏏",
    layout="wide"
)

apply_custom_style()
apply_page_accent("#1A237E")

st.title("🏏 Cricbuzz LiveStats")
st.subheader("Real-Time Cricket Insights & SQL-Based Analytics")

st.markdown("""
Welcome! This dashboard integrates live cricket data from the Cricbuzz API
with a MySQL database to deliver:

- ⚡ **Live Match** — live scores and detailed scorecards (batsmen/bowler info)
- 📊 **Top Player Stats** — batting and bowling leaderboards
- 🔍 **SQL Analytics** — 25 practice queries across beginner, intermediate,
  and advanced levels
- 🛠️ **CRUD Operations** — manage player and match records directly

Use the sidebar on the left to navigate between pages.
""")

st.divider()

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Tools Used", "Python, SQL, Streamlit")
with col2:
    st.metric("SQL Queries", "25")
with col3:
    st.metric("Data Source", "Cricbuzz API")

st.divider()

# ---------------- Instructions ----------------
st.header("📖 How to Use This Dashboard")
st.markdown("""
1. **Live Match** — See currently live/recent matches. Select a match from the
   dropdown to view its full scorecard, including individual batsman and
   bowler statistics.
2. **Top Player Stats** — Choose a stat category (Most Runs, Most Wickets,
   Highest Score, etc.) from the dropdown to see the current leaderboard.
3. **SQL Analytics** — Pick any of the 25 queries from the dropdown, expand
   "View SQL" to see the query itself, and click **Run Query** to see live
   results from the project's MySQL database.
4. **CRUD Operations** — Switch between the **Players** and **Matches** tabs,
   then use Create / Read / Update / Delete to manage records directly in
   the database.
""")

st.divider()

# ---------------- Documentation & folder structure ----------------
st.header("📂 Project Documentation & Folder Structure")
st.markdown("""
Full setup instructions, environment variables, and API details are in the
project's **README.md** file at the root of the repository.
""")

with st.expander("📁 View project folder structure"):
    st.code("""
CricbuzzLiveStats/
├── __pycache__
├── .streamlit
│   └──config.toml           # Global theme (dark background, accent color, font)
├── .env                     # API keys & DB credentials (not committed)
├── .gitignore
├── requirements.txt
├── api_client.py            # Cricbuzz API wrapper functions
├── home.py                  # Home page (Streamlit entry point)
├── generate_seed_data.py    # Engineered seed data generator
├── README.md
├── utils/
│   ├── __pycache__
│   ├── styling.py           # Shared CSS + per-page accent colors/backgrounds
│   ├── config.py            # Reads secrets from .env (local) or st.secrets (Streamlit Cloud)
│   └── db_connection.py     # MySQL connection helper (works with local MySQL or Aiven)
├── pages/            
│   ├── 1_Live_Match.py
│   ├── 2_Top_Player_Stats.py
│   ├── 3_SQL_Analytics.py
│   ├── 4_CRUD_Operations.py    
│   ├── 5_Visualizations.py
│   └── 6_Conclusion.py
├── sql/
│   ├── schema_mysql.sql     # Database schema (CREATE TABLE statements)
│   ├── seed_data.sql        # Initial small seed dataset
│   └── all_25_queries.sql   # All 25 SQL queries as standalone reference
└── sample_data/
    ├── recent_matches.json  # Saved API response samples (for offline dev)
    └── scorecard.json
    """, language="text")

st.divider()
st.caption("Built as part of the Cricbuzz LiveStats project. See the Conclusion page for insights, recommendations, and limitations.")