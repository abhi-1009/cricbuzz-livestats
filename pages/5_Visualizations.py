import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.styling import apply_custom_style, apply_page_accent
from utils.db_connection import get_connection

st.set_page_config(page_title="Visualizations", page_icon="📈", layout="wide")

apply_custom_style()
apply_page_accent("#2E7D32")

st.title("📈 Cricket Visualizations")
st.caption("Quick visual insights from the project database.")

def run_query(query):
    conn = get_connection()
    if conn is None:
        return None
    cursor = conn.cursor(dictionary=True)
    cursor.execute(query)
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return pd.DataFrame(rows)


col1, col2 = st.columns(2)

# ---------------- Chart 1: Total wins by team ----------------
with col1:
    st.subheader("🏆 Total Wins by Team")
    df_wins = run_query("""
        SELECT t.team_name, COUNT(*) AS total_wins
        FROM matches m
        JOIN teams t ON m.winner_team_id = t.team_id
        GROUP BY t.team_id, t.team_name
        ORDER BY total_wins DESC
    """)
    if df_wins is not None and not df_wins.empty:
        st.bar_chart(df_wins.set_index("team_name")["total_wins"])
    else:
        st.info("No data available.")

# ---------------- Chart 2: Matches by format ----------------
with col2:
    st.subheader("🎯 Matches by Format")
    df_format = run_query("""
        SELECT format, COUNT(*) AS match_count
        FROM matches
        GROUP BY format
    """)
    if df_format is not None and not df_format.empty:
        fig, ax = plt.subplots()
        ax.pie(df_format["match_count"], labels=df_format["format"], autopct="%1.1f%%", startangle=90)
        ax.axis("equal")
        st.pyplot(fig)
    else:
        st.info("No data available.")

st.divider()

col3, col4 = st.columns(2)

# ---------------- Chart 3: Player role distribution ----------------
with col3:
    st.subheader("👥 Player Role Distribution")
    df_roles = run_query("""
        SELECT playing_role, COUNT(*) AS player_count
        FROM players
        GROUP BY playing_role
    """)
    if df_roles is not None and not df_roles.empty:
        fig, ax = plt.subplots()
        ax.pie(df_roles["player_count"], labels=df_roles["playing_role"], autopct="%1.1f%%", startangle=90)
        ax.axis("equal")
        st.pyplot(fig)
    else:
        st.info("No data available.")

# ---------------- Chart 4: Toss decision win rate ----------------
with col4:
    st.subheader("🪙 Toss Decision Win Rate")
    df_toss = run_query("""
        SELECT m.toss_decision,
               ROUND(100 * SUM(CASE WHEN m.toss_winner_id = m.winner_team_id THEN 1 ELSE 0 END) / COUNT(*), 2) AS win_pct
        FROM matches m
        WHERE m.toss_decision IS NOT NULL AND m.winner_team_id IS NOT NULL
        GROUP BY m.toss_decision
    """)
    if df_toss is not None and not df_toss.empty:
        st.bar_chart(df_toss.set_index("toss_decision")["win_pct"])
        st.caption("% of matches won by the team that won the toss, split by their decision (bat/bowl first).")
    else:
        st.info("No data available.")

st.divider()

# ---------------- Chart 5: Top 10 run scorers (ODI) ----------------
st.subheader("🏏 Top 10 ODI Run Scorers")
df_runs = run_query("""
    SELECT p.full_name, SUM(b.runs_scored) AS total_runs
    FROM batting_stats b
    JOIN matches m ON b.match_id = m.match_id
    JOIN players p ON b.player_id = p.player_id
    WHERE m.format = 'ODI'
    GROUP BY p.player_id, p.full_name
    ORDER BY total_runs DESC
    LIMIT 10
""")
if df_runs is not None and not df_runs.empty:
    st.bar_chart(df_runs.set_index("full_name")["total_runs"])
else:
    st.info("No data available.")

st.caption("All charts reflect the current state of the MySQL database.")