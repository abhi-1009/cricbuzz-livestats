import streamlit as st
import pandas as pd
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.styling import apply_custom_style, apply_page_accent
from utils.db_connection import get_connection

st.set_page_config(page_title="CRUD Operations", page_icon="🛠️", layout="wide")

apply_custom_style()
apply_page_accent("#00838F")

st.title("🛠️ CRUD Operations")
st.caption("Create, Read, Update, and Delete player and match records directly in the database.")

def run_query(query, params=None, fetch=False):
    conn = get_connection()
    if conn is None:
        st.error("Could not connect to the database.")
        return None
    try:
        with conn:
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute(query, params or ())
                if fetch:
                    return cursor.fetchall()
                conn.commit()
                return cursor.rowcount
    except Exception as e:
        st.error(f"Database error: {e}")
        return None
    finally:
        conn.close()

def get_lookup(query):
    """Returns list of (id, label) tuples for dropdowns."""
    rows = run_query(query, fetch=True)
    return rows if rows else []


entity = st.tabs(["👤 Players", "🏏 Matches"])

# ================================================================
# PLAYERS TAB
# ================================================================
with entity[0]:
    operation = st.radio("Operation", ["Create", "Read", "Update", "Delete"], horizontal=True, key="player_op")

    # ---------------- CREATE ----------------
    if operation == "Create":
        st.subheader("Add a New Player")
        with st.form("create_player_form"):
            full_name = st.text_input("Full Name *")
            country = st.text_input("Country *")
            playing_role = st.selectbox("Playing Role", ["Batsman", "Bowler", "All-rounder", "Wicket-keeper"])
            batting_style = st.selectbox("Batting Style", ["Right-hand bat", "Left-hand bat", "N/A"])
            bowling_style = st.text_input("Bowling Style (leave blank if none)")

            submitted = st.form_submit_button("➕ Add Player")
            if submitted:
                if not full_name or not country:
                    st.warning("Full Name and Country are required.")
                else:
                    result = run_query(
                        """INSERT INTO players (full_name, country, playing_role, batting_style, bowling_style)
                           VALUES (%s, %s, %s, %s, %s)""",
                        (full_name, country, playing_role,
                         None if batting_style == "N/A" else batting_style,
                         bowling_style if bowling_style else None)
                    )
                    if result is not None:
                        st.success(f"Player '{full_name}' added successfully.")

    # ---------------- READ ----------------
    elif operation == "Read":
        st.subheader("View / Search Players")
        col1, col2 = st.columns(2)
        with col1:
            search_name = st.text_input("Search by name (leave blank for all)")
        with col2:
            filter_country = st.text_input("Filter by country (leave blank for all)")

        query = "SELECT player_id, full_name, country, playing_role, batting_style, bowling_style FROM players WHERE 1=1"
        params = []
        if search_name:
            query += " AND full_name LIKE %s"
            params.append(f"%{search_name}%")
        if filter_country:
            query += " AND country LIKE %s"
            params.append(f"%{filter_country}%")
        query += " ORDER BY full_name"

        rows = run_query(query, params, fetch=True)
        if rows:
            st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
            st.caption(f"{len(rows)} player(s) found.")
        else:
            st.info("No players found.")

    # ---------------- UPDATE ----------------
    elif operation == "Update":
        st.subheader("Update a Player")
        players = get_lookup("SELECT player_id, full_name FROM players ORDER BY full_name")
        if not players:
            st.info("No players in the database yet.")
        else:
            options = {f"{p['full_name']} (ID {p['player_id']})": p['player_id'] for p in players}
            selected_label = st.selectbox("Select player to update", options=list(options.keys()))
            selected_id = options[selected_label]

            current = run_query("SELECT * FROM players WHERE player_id = %s", (selected_id,), fetch=True)
            if current:
                current = current[0]
                with st.form("update_player_form"):
                    full_name = st.text_input("Full Name", value=current["full_name"])
                    country = st.text_input("Country", value=current["country"])
                    roles = ["Batsman", "Bowler", "All-rounder", "Wicket-keeper"]
                    playing_role = st.selectbox("Playing Role", roles,
                                                 index=roles.index(current["playing_role"]) if current["playing_role"] in roles else 0)
                    batting_style = st.text_input("Batting Style", value=current["batting_style"] or "")
                    bowling_style = st.text_input("Bowling Style", value=current["bowling_style"] or "")

                    submitted = st.form_submit_button("💾 Save Changes")
                    if submitted:
                        result = run_query(
                            """UPDATE players SET full_name=%s, country=%s, playing_role=%s,
                               batting_style=%s, bowling_style=%s WHERE player_id=%s""",
                            (full_name, country, playing_role,
                             batting_style or None, bowling_style or None, selected_id)
                        )
                        if result is not None:
                            st.success(f"Player '{full_name}' updated successfully.")

    # ---------------- DELETE ----------------
    elif operation == "Delete":
        st.subheader("Delete a Player")
        players = get_lookup("SELECT player_id, full_name FROM players ORDER BY full_name")
        if not players:
            st.info("No players in the database yet.")
        else:
            options = {f"{p['full_name']} (ID {p['player_id']})": p['player_id'] for p in players}
            selected_label = st.selectbox("Select player to delete", options=list(options.keys()), key="delete_player_select")
            selected_id = options[selected_label]

            st.warning(f"This will permanently delete **{selected_label}**.")
            confirm = st.checkbox("I understand this cannot be undone.")
            if st.button("🗑️ Delete Player", disabled=not confirm):
                result = run_query("DELETE FROM players WHERE player_id = %s", (selected_id,))
                if result is not None:
                    if result > 0:
                        st.success("Player deleted successfully.")
                        st.rerun()
                    else:
                        st.info("No player was deleted.")


# ================================================================
# MATCHES TAB
# ================================================================
with entity[1]:
    operation = st.radio("Operation", ["Create", "Read", "Update", "Delete"], horizontal=True, key="match_op")

    teams = get_lookup("SELECT team_id, team_name FROM teams ORDER BY team_name")
    venues = get_lookup("SELECT venue_id, venue_name FROM venues ORDER BY venue_name")
    series = get_lookup("SELECT series_id, series_name FROM series ORDER BY series_name")

    team_options = {t["team_name"]: t["team_id"] for t in teams} if teams else {}
    venue_options = {v["venue_name"]: v["venue_id"] for v in venues} if venues else {}
    series_options = {s["series_name"]: s["series_id"] for s in series} if series else {}

    # ---------------- CREATE ----------------
    if operation == "Create":
        st.subheader("Add a New Match")
        if not team_options or not venue_options or not series_options:
            st.warning("You need at least one team, venue, and series in the database before adding a match.")
        else:
            with st.form("create_match_form"):
                series_name = st.selectbox("Series", options=list(series_options.keys()))
                match_desc = st.text_input("Match Description (e.g. '3rd ODI')")
                match_format = st.selectbox("Format", ["Test", "ODI", "T20I"])
                team1_name = st.selectbox("Team 1", options=list(team_options.keys()))
                team2_name = st.selectbox("Team 2", options=list(team_options.keys()), index=1 if len(team_options) > 1 else 0)
                venue_name = st.selectbox("Venue", options=list(venue_options.keys()))
                match_date = st.date_input("Match Date")
                toss_winner_name = st.selectbox("Toss Winner", options=list(team_options.keys()))
                toss_decision = st.selectbox("Toss Decision", ["bat", "bowl"])
                winner_name = st.selectbox("Match Winner (if completed)", options=["Not decided yet"] + list(team_options.keys()))
                victory_type = st.selectbox("Victory Type", ["N/A", "runs", "wickets"])
                victory_margin = st.number_input("Victory Margin", min_value=0, step=1)

                submitted = st.form_submit_button("➕ Add Match")
                if submitted:
                    if team1_name == team2_name:
                        st.warning("Team 1 and Team 2 must be different.")
                    else:
                        result = run_query(
                            """INSERT INTO matches (series_id, match_desc, format, team1_id, team2_id,
                               venue_id, match_date, toss_winner_id, toss_decision, winner_team_id,
                               victory_margin, victory_type)
                               VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
                            (series_options[series_name], match_desc, match_format,
                             team_options[team1_name], team_options[team2_name],
                             venue_options[venue_name], match_date,
                             team_options[toss_winner_name], toss_decision,
                             None if winner_name == "Not decided yet" else team_options[winner_name],
                             victory_margin, None if victory_type == "N/A" else victory_type)
                        )
                        if result is not None:
                            st.success("Match added successfully.")

    # ---------------- READ ----------------
    elif operation == "Read":
        st.subheader("View / Search Matches")
        col1, col2 = st.columns(2)
        with col1:
            filter_format = st.selectbox("Filter by format", ["All", "Test", "ODI", "T20I"])
        with col2:
            filter_team = st.selectbox("Filter by team", ["All"] + list(team_options.keys()))

        query = """
            SELECT m.match_id, m.match_desc, m.format, t1.team_name AS team1, t2.team_name AS team2,
                   v.venue_name, m.match_date, tw.team_name AS winner, m.victory_margin, m.victory_type
            FROM matches m
            JOIN teams t1 ON m.team1_id = t1.team_id
            JOIN teams t2 ON m.team2_id = t2.team_id
            JOIN venues v ON m.venue_id = v.venue_id
            LEFT JOIN teams tw ON m.winner_team_id = tw.team_id
            WHERE 1=1
        """
        params = []
        if filter_format != "All":
            query += " AND m.format = %s"
            params.append(filter_format)
        if filter_team != "All":
            query += " AND (t1.team_name = %s OR t2.team_name = %s)"
            params.extend([filter_team, filter_team])
        query += " ORDER BY m.match_date DESC LIMIT 100"

        rows = run_query(query, params, fetch=True)
        if rows:
            st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
            st.caption(f"{len(rows)} match(es) found (showing up to 100).")
        else:
            st.info("No matches found.")

    # ---------------- UPDATE ----------------
    elif operation == "Update":
        st.subheader("Update a Match")
        matches = get_lookup(
            "SELECT match_id, match_desc, match_date FROM matches ORDER BY match_date DESC LIMIT 200"
        )
        if not matches:
            st.info("No matches in the database yet.")
        else:
            options = {f"{m['match_desc']} — {m['match_date']} (ID {m['match_id']})": m['match_id'] for m in matches}
            selected_label = st.selectbox("Select match to update", options=list(options.keys()))
            selected_id = options[selected_label]

            current = run_query("SELECT * FROM matches WHERE match_id = %s", (selected_id,), fetch=True)
            if current:
                current = current[0]
                with st.form("update_match_form"):
                    match_desc = st.text_input("Match Description", value=current["match_desc"] or "")
                    formats = ["Test", "ODI", "T20I"]
                    match_format = st.selectbox("Format", formats, index=formats.index(current["format"]) if current["format"] in formats else 0)
                    winner_name = st.selectbox(
                        "Match Winner",
                        options=["Not decided yet"] + list(team_options.keys()),
                    )
                    victory_type = st.selectbox("Victory Type", ["N/A", "runs", "wickets"])
                    victory_margin = st.number_input("Victory Margin", min_value=0, step=1,
                                                       value=int(current["victory_margin"]) if current["victory_margin"] else 0)

                    submitted = st.form_submit_button("💾 Save Changes")
                    if submitted:
                        result = run_query(
                            """UPDATE matches SET match_desc=%s, format=%s, winner_team_id=%s,
                               victory_type=%s, victory_margin=%s WHERE match_id=%s""",
                            (match_desc, match_format,
                             None if winner_name == "Not decided yet" else team_options[winner_name],
                             None if victory_type == "N/A" else victory_type,
                             victory_margin, selected_id)
                        )
                        if result is not None:
                            st.success("Match updated successfully.")

    # ---------------- DELETE ----------------
    elif operation == "Delete":
        st.subheader("Delete a Match")
        matches = get_lookup(
            "SELECT match_id, match_desc, match_date FROM matches ORDER BY match_date DESC LIMIT 200"
        )
        if not matches:
            st.info("No matches in the database yet.")
        else:
            options = {f"{m['match_desc']} — {m['match_date']} (ID {m['match_id']})": m['match_id'] for m in matches}
            selected_label = st.selectbox("Select match to delete", options=list(options.keys()), key="delete_match_select")
            selected_id = options[selected_label]

            st.warning(f"This will permanently delete **{selected_label}** and cannot be undone.")
            st.caption("Note: if this match has related batting/bowling/fielding stats, deletion will fail "
                       "due to database constraints — delete those stat rows first if needed.")
            confirm = st.checkbox("I understand this cannot be undone.", key="confirm_match_delete")
            if st.button("🗑️ Delete Match", disabled=not confirm):
                result = run_query("DELETE FROM matches WHERE match_id = %s", (selected_id,))
                if result is not None:
                    if result > 0:
                        st.success("Match deleted successfully.")
                        st.rerun()
                    else:
                        st.info("No match was deleted.")