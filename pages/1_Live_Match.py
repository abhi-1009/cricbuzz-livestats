import streamlit as st
import pandas as pd
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.styling import apply_custom_style, apply_page_accent
from api_client import get_live_matches, get_scorecard

st.set_page_config(page_title="Live Match", page_icon="⚡", layout="wide")

apply_custom_style()
apply_page_accent("#D32F2F")

# st.title("⚡ Live Match")
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from api_client import get_live_matches, get_scorecard

st.set_page_config(page_title="Live Match", page_icon="⚡", layout="wide")
st.title("⚡ Live Match")


@st.cache_data(ttl=300)
def load_live_matches():
    return get_live_matches()


@st.cache_data(ttl=300)
def load_scorecard(match_id):
    return get_scorecard(match_id)


data = load_live_matches()

match_options = {}  # label -> match_id

if not data or "typeMatches" not in data:
    st.warning("No live match data available right now. Try refreshing in a bit.")
else:
    for type_match in data["typeMatches"]:
        match_type = type_match.get("matchType", "Matches")
        series_list = type_match.get("seriesMatches", [])
        real_series = [s for s in series_list if "seriesAdWrapper" in s]
        if not real_series:
            continue

        st.header(match_type)

        for series in real_series:
            wrapper = series["seriesAdWrapper"]
            series_name = wrapper.get("seriesName", "Series")
            matches = wrapper.get("matches", [])

            st.subheader(series_name)

            for m in matches:
                info = m.get("matchInfo", {})
                score = m.get("matchScore", {})

                match_id = info.get("matchId")
                team1 = info.get("team1", {}).get("teamName", "Team 1")
                team2 = info.get("team2", {}).get("teamName", "Team 2")
                venue = info.get("venueInfo", {}).get("ground", "")
                city = info.get("venueInfo", {}).get("city", "")
                status = info.get("status", "")
                match_desc = info.get("matchDesc", "")
                match_format = info.get("matchFormat", "")

                label = f"{team1} vs {team2} — {match_desc} ({series_name})"
                if match_id:
                    match_options[label] = match_id

                with st.container(border=True):
                    col1, col2 = st.columns([3, 2])

                    with col1:
                        st.markdown(f"**{team1} vs {team2}**")
                        st.caption(f"{match_desc} · {match_format} · {venue}, {city}")

                        t1_score = score.get("team1Score", {}).get("inngs1", {})
                        t2_score = score.get("team2Score", {}).get("inngs1", {})

                        if t1_score:
                            st.text(
                                f"{team1}: {t1_score.get('runs', 0)}/{t1_score.get('wickets', 0)} "
                                f"({t1_score.get('overs', 0)} overs)"
                            )
                        if t2_score:
                            st.text(
                                f"{team2}: {t2_score.get('runs', 0)}/{t2_score.get('wickets', 0)} "
                                f"({t2_score.get('overs', 0)} overs)"
                            )

                    with col2:
                        st.info(status)

st.divider()
if st.button("🔄 Refresh match list (uses 1 API call)"):
    st.cache_data.clear()
    st.rerun()

# ============================================================
# Detailed scorecard section
# ============================================================
st.divider()
st.header("📋 Detailed Scorecard")

if not match_options:
    st.info("No matches available to view a scorecard for right now.")
else:
    selected_label = st.selectbox("Select a match", options=list(match_options.keys()))
    selected_match_id = match_options[selected_label]

    if st.button("🔍 Load Scorecard (uses 1 API call)"):
        scorecard_data = load_scorecard(selected_match_id)

        if not scorecard_data or not scorecard_data.get("scorecard"):
            st.warning("Scorecard not available yet — the match may not have started, or is between innings.")
        else:
            for innings in scorecard_data["scorecard"]:
                team_name = innings.get("batteamname", "Innings")
                score = innings.get("score", 0)
                wickets = innings.get("wickets", 0)
                overs = innings.get("overs", 0)

                st.subheader(f"{team_name} — {score}/{wickets} ({overs} overs)")

                # Batting table
                batsmen = innings.get("batsman", [])
                if batsmen:
                    bat_rows = []
                    for b in batsmen:
                        bat_rows.append({
                            "Batsman": b.get("name", ""),
                            "Runs": b.get("runs", 0),
                            "Balls": b.get("balls", 0),
                            "4s": b.get("fours", 0),
                            "6s": b.get("sixes", 0),
                            "SR": b.get("strkrate", ""),
                            "Dismissal": b.get("outdec", "not out") or "not out",
                        })
                    st.dataframe(pd.DataFrame(bat_rows), use_container_width=True, hide_index=True)

                # Bowling table
                bowlers = innings.get("bowler", [])
                if bowlers:
                    bowl_rows = []
                    for bo in bowlers:
                        bowl_rows.append({
                            "Bowler": bo.get("name", ""),
                            "Overs": bo.get("overs", 0),
                            "Maidens": bo.get("maidens", 0),
                            "Runs": bo.get("runs", 0),
                            "Wickets": bo.get("wickets", 0),
                            "Economy": bo.get("economy", ""),
                        })
                    st.caption("Bowling")
                    st.dataframe(pd.DataFrame(bowl_rows), use_container_width=True, hide_index=True)

                st.divider()