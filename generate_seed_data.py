"""
Cricbuzz LiveStats — Expanded Seed Data Generator
====================================================
Run this ONCE from your project root: python generate_seed_data.py
"""
import random
from datetime import date, timedelta
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from utils.db_connection import get_connection

random.seed(42)

conn = get_connection()
if conn is None:
    print("Could not connect to database. Check your .env file.")
    sys.exit(1)

cursor = conn.cursor()

# ============================================================
# STEP 1: Clear existing data (children first, respecting FKs)
# ============================================================
print("Clearing existing data...")
for table in ["fielding_stats", "bowling_stats", "batting_stats", "matches",
              "series", "players", "venues", "teams"]:
    cursor.execute(f"DELETE FROM {table}")
    cursor.execute(f"ALTER TABLE {table} AUTO_INCREMENT = 1")
conn.commit()

# ============================================================
# STEP 2: Teams
# ============================================================
print("Inserting teams...")
teams_data = [
    ("India", "India"), ("Australia", "Australia"), ("England", "England"),
    ("Pakistan", "Pakistan"), ("South Africa", "South Africa"),
    ("New Zealand", "New Zealand"), ("Sri Lanka", "Sri Lanka"),
    ("West Indies", "West Indies"),
]
cursor.executemany("INSERT INTO teams (team_name, country) VALUES (%s, %s)", teams_data)
conn.commit()
cursor.execute("SELECT team_id, team_name FROM teams")
TEAM_ID = {name: tid for tid, name in cursor.fetchall()}

# ============================================================
# STEP 3: Venues
# ============================================================
print("Inserting venues...")
venues_data = [
    ("Eden Gardens", "Kolkata", "India", 68000),
    ("Melbourne Cricket Ground", "Melbourne", "Australia", 100024),
    ("Lord's", "London", "England", 30000),
    ("Gaddafi Stadium", "Lahore", "Pakistan", 27000),
    ("Wanderers Stadium", "Johannesburg", "South Africa", 34000),
    ("Eden Park", "Auckland", "New Zealand", 50000),
    ("R Premadasa Stadium", "Colombo", "Sri Lanka", 35000),
    ("Kensington Oval", "Bridgetown", "West Indies", 28000),
]
cursor.executemany(
    "INSERT INTO venues (venue_name, city, country, capacity) VALUES (%s, %s, %s, %s)",
    venues_data
)
conn.commit()
cursor.execute("SELECT venue_id, country FROM venues")
VENUE_BY_COUNTRY = {}
for vid, country in cursor.fetchall():
    VENUE_BY_COUNTRY[country] = vid

# ============================================================
# STEP 4: Series
# ============================================================
print("Inserting series...")
series_data = [
    ("India tour of Australia 2020", "Australia", "ODI", "2020-01-10", 4),
    ("India tour of England 2021", "England", "Mixed", "2021-06-01", 5),
    ("India tour of South Africa 2022", "South Africa", "ODI", "2022-01-15", 4),
    ("India tour of New Zealand 2023", "New Zealand", "ODI", "2023-02-01", 4),
    ("India vs Australia ODI Series 2024", "India", "ODI", "2024-01-05", 4),
    ("India vs Australia ODI Series 2025", "Australia", "ODI", "2025-02-10", 3),
    ("ICC World Cup 2023", "India", "ODI", "2023-10-05", 10),
    ("The Ashes 2023", "England", "Test", "2023-06-16", 5),
    ("T20 Tri-Series 2024", "South Africa", "T20I", "2024-01-10", 6),
    ("World T20 2026", "West Indies", "T20I", "2026-06-01", 10),
    ("India tour of Sri Lanka 2021", "Sri Lanka", "ODI", "2021-07-01", 3),
    ("India tour of West Indies 2022", "West Indies", "T20I", "2022-08-01", 3),
]
cursor.executemany(
    "INSERT INTO series (series_name, host_country, match_type, start_date, total_matches) "
    "VALUES (%s, %s, %s, %s, %s)",
    series_data
)
conn.commit()
cursor.execute("SELECT series_id, series_name FROM series")
SERIES_ID = {name: sid for sid, name in cursor.fetchall()}

# ============================================================
# STEP 5: Players
# ============================================================
print("Inserting players...")
players_data = [
    # India
    ("Rohan Verma", "India", "Batsman", "Right-hand bat", None),
    ("Arjun Mehta", "India", "All-rounder", "Right-hand bat", "Right-arm medium"),
    ("Vikram Nair", "India", "Bowler", "Right-hand bat", "Right-arm fast"),
    ("Suresh Iyer", "India", "Batsman", "Left-hand bat", None),
    ("Karan Thakur", "India", "Wicket-keeper", "Right-hand bat", None),
    ("Aditya Rao", "India", "Bowler", "Right-hand bat", "Left-arm orthodox"),
    # Australia
    ("Steven Clarke", "Australia", "Batsman", "Left-hand bat", None),
    ("Mitchell Grant", "Australia", "Bowler", "Right-hand bat", "Left-arm fast"),
    ("Liam Foster", "Australia", "Batsman", "Right-hand bat", None),
    ("Ryan Cole", "Australia", "All-rounder", "Right-hand bat", "Right-arm off break"),
    # England
    ("Joe Bentley", "England", "Batsman", "Right-hand bat", None),
    ("Sam Wood", "England", "All-rounder", "Left-hand bat", "Right-arm off break"),
    ("Harry Pike", "England", "Bowler", "Right-hand bat", "Right-arm fast-medium"),
    # Pakistan
    ("Imran Sheikh", "Pakistan", "All-rounder", "Right-hand bat", "Left-arm orthodox"),
    ("Faisal Khan", "Pakistan", "Bowler", "Right-hand bat", "Right-arm fast"),
    ("Ahmed Raza", "Pakistan", "Batsman", "Left-hand bat", None),
    # South Africa
    ("Dean Roberts", "South Africa", "Wicket-keeper", "Right-hand bat", None),
    ("Luke Adams", "South Africa", "Batsman", "Right-hand bat", None),
    ("Chris Botha", "South Africa", "Bowler", "Right-hand bat", "Right-arm fast"),
    # New Zealand
    ("Kane Wilson", "New Zealand", "Batsman", "Left-hand bat", None),
    ("Trent Foster", "New Zealand", "Bowler", "Right-hand bat", "Right-arm fast-medium"),
    ("Josh Miller", "New Zealand", "All-rounder", "Right-hand bat", "Right-arm medium"),
    # Sri Lanka
    ("Nuwan Silva", "Sri Lanka", "Batsman", "Left-hand bat", None),
    ("Dinesh Perera", "Sri Lanka", "Bowler", "Right-hand bat", "Left-arm spin"),
    # West Indies
    ("Andre Baptiste", "West Indies", "Batsman", "Right-hand bat", None),
    ("Marcus James", "West Indies", "Bowler", "Right-hand bat", "Right-arm fast"),
]
cursor.executemany(
    "INSERT INTO players (full_name, country, playing_role, batting_style, bowling_style) "
    "VALUES (%s, %s, %s, %s, %s)",
    players_data
)
conn.commit()
cursor.execute("SELECT player_id, full_name FROM players")
PLAYER_ID = {name: pid for pid, name in cursor.fetchall()}

OPPONENTS = ["Australia", "England", "Pakistan", "South Africa", "New Zealand", "Sri Lanka", "West Indies"]


def random_date_in_quarter(year, quarter):
    q_start_month = (quarter - 1) * 3 + 1
    start = date(year, q_start_month, 1)
    end_month = q_start_month + 2
    end_year = year
    if end_month > 12:
        end_month -= 12
        end_year += 1
    if end_month == 12:
        end = date(end_year, 12, 31)
    else:
        end = date(end_year, end_month + 1, 1) - timedelta(days=1)
    delta = (end - start).days
    return start + timedelta(days=random.randint(0, max(delta, 0)))


def insert_match(series_id, match_desc, fmt, team1, team2, venue_country, match_date,
                  toss_winner=None, toss_decision=None, winner=None, margin=None, vtype=None):
    if toss_winner is None:
        toss_winner = random.choice([team1, team2])
    if toss_decision is None:
        toss_decision = random.choice(["bat", "bowl"])
    if winner is None:
        winner = random.choice([team1, team2])
    if vtype is None:
        vtype = random.choice(["runs", "wickets"])
    if margin is None:
        margin = random.randint(1, 90) if vtype == "runs" else random.randint(1, 9)

    cursor.execute(
        """INSERT INTO matches (series_id, match_desc, format, team1_id, team2_id, venue_id,
           match_date, toss_winner_id, toss_decision, winner_team_id, victory_margin, victory_type)
           VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
        (series_id, match_desc, fmt, TEAM_ID[team1], TEAM_ID[team2], VENUE_BY_COUNTRY[venue_country],
         match_date, TEAM_ID[toss_winner], toss_decision, TEAM_ID[winner], margin, vtype)
    )
    return cursor.lastrowid


def insert_batting(match_id, player_name, innings_no, position, runs, balls, fours, sixes):
    sr = round((runs / balls) * 100, 2) if balls > 0 else 0
    dismissal = "not out" if random.random() < 0.15 else random.choice(
        ["caught", "bowled", "lbw", "run out", "stumped"])
    if dismissal == "not out":
        dismissal = "not out"
    cursor.execute(
        """INSERT INTO batting_stats (match_id, player_id, innings_no, batting_position,
           runs_scored, balls_faced, fours, sixes, strike_rate, dismissal_type)
           VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
        (match_id, PLAYER_ID[player_name], innings_no, position, runs, balls, fours, sixes, sr, dismissal)
    )


def insert_bowling(match_id, player_name, innings_no, overs, runs_conceded, wickets):
    econ = round(runs_conceded / overs, 2) if overs > 0 else 0
    cursor.execute(
        """INSERT INTO bowling_stats (match_id, player_id, innings_no, overs_bowled,
           runs_conceded, wickets_taken, economy_rate)
           VALUES (%s,%s,%s,%s,%s,%s,%s)""",
        (match_id, PLAYER_ID[player_name], innings_no, overs, runs_conceded, wickets, econ)
    )


def insert_fielding(match_id, player_name, catches, stumpings, run_outs):
    cursor.execute(
        """INSERT INTO fielding_stats (match_id, player_id, catches, stumpings, run_outs)
           VALUES (%s,%s,%s,%s,%s)""",
        (match_id, PLAYER_ID[player_name], catches, stumpings, run_outs)
    )


# ============================================================
# STEP 6: Arjun Mehta's 36 engineered ODI matches
# 6 years x 2 quarters x 3 matches = 36 matches
# -> satisfies Q9, Q16, Q20, Q25
# ============================================================
print("Generating Arjun Mehta's career matches (Q9, Q16, Q20, Q25)...")
years_quarters = [(y, q) for y in range(2020, 2026) for q in (1, 3)]

for (year, quarter) in years_quarters:
    for i in range(3):
        # Route India-vs-Australia matches through 2024-2025 for Q22
        if year in (2024, 2025):
            opponent = "Australia"
        else:
            opponent = random.choice([o for o in OPPONENTS if o != "Australia"])

        mdate = random_date_in_quarter(year, quarter)
        match_id = insert_match(
            SERIES_ID["India vs Australia ODI Series 2024"] if opponent == "Australia" and year == 2024
            else SERIES_ID["India vs Australia ODI Series 2025"] if opponent == "Australia"
            else SERIES_ID["India tour of Australia 2020"],
            f"ODI vs {opponent}", "ODI", "India", opponent, opponent, mdate
        )

        # Batting lineup
        arjun_runs = random.randint(45, 90)
        arjun_balls = random.randint(40, 75)
        insert_batting(match_id, "Rohan Verma", 1, 1, random.randint(10, 80), random.randint(15, 90), random.randint(0, 8), random.randint(0, 3))
        insert_batting(match_id, "Arjun Mehta", 1, 2, arjun_runs, arjun_balls, random.randint(2, 8), random.randint(0, 4))
        insert_batting(match_id, "Suresh Iyer", 1, 3, random.randint(5, 60), random.randint(10, 70), random.randint(0, 6), random.randint(0, 2))
        insert_batting(match_id, "Karan Thakur", 1, 4, random.randint(5, 45), random.randint(10, 50), random.randint(0, 4), random.randint(0, 1))

        # Bowling: Arjun bowls (wickets 3-5 to guarantee >50 total across 36 matches)
        arjun_wkts = random.randint(3, 5)
        arjun_overs = 10
        arjun_runs_conceded = random.randint(30, 55)
        insert_bowling(match_id, "Arjun Mehta", 2, arjun_overs, arjun_runs_conceded, arjun_wkts)
        insert_bowling(match_id, "Vikram Nair", 2, 9, random.randint(30, 50), random.randint(1, 4))

        # Fielding (light)
        if random.random() < 0.4:
            insert_fielding(match_id, "Karan Thakur", random.randint(0, 2), random.randint(0, 1), 0)

conn.commit()

# ============================================================
# STEP 7: Vikram Nair's dedicated economical-bowler matches (Q18)
# 15 matches (mix ODI/T20I), tight economy, vs varied opponents
# ============================================================
print("Generating Vikram Nair's economical bowling matches (Q18)...")
for i in range(15):
    fmt = random.choice(["ODI", "T20I"])
    opponent = random.choice(OPPONENTS)
    year = random.randint(2022, 2026)
    mdate = date(year, random.randint(1, 12), random.randint(1, 28))
    match_id = insert_match(
        SERIES_ID["India tour of New Zealand 2023"], f"{fmt} vs {opponent}", fmt,
        "India", opponent, opponent, mdate
    )
    overs = 10 if fmt == "ODI" else 4
    runs_conceded = random.randint(int(overs * 3.2), int(overs * 4.5))  # tight economy
    insert_bowling(match_id, "Vikram Nair", 2, overs, runs_conceded, random.randint(1, 3))
    insert_batting(match_id, "Rohan Verma", 1, 1, random.randint(10, 70), random.randint(15, 80), random.randint(0, 6), random.randint(0, 2))

conn.commit()

# ============================================================
# STEP 8: ~70 additional randomized matches for general variety
# (partnerships, close matches, toss data, home/away, formats)
# ============================================================
print("Generating additional randomized matches for variety...")
all_countries = ["India", "Australia", "England", "Pakistan", "South Africa",
                  "New Zealand", "Sri Lanka", "West Indies"]
country_players = {}
for name, country, *_ in players_data:
    country_players.setdefault(country, []).append(name)

fallback_series = SERIES_ID["ICC World Cup 2023"]

for i in range(70):
    team1, team2 = random.sample(all_countries, 2)
    fmt = random.choice(["Test", "ODI", "T20I"])
    year = random.randint(2019, 2026)
    mdate = date(year, random.randint(1, 12), random.randint(1, 28))
    venue_country = random.choice([team1, team2])

    # Occasionally force a close match (for Q15)
    if random.random() < 0.3:
        vtype = random.choice(["runs", "wickets"])
        margin = random.randint(1, 45) if vtype == "runs" else random.randint(1, 4)
    else:
        vtype = None
        margin = None

    match_id = insert_match(fallback_series, f"Match {i+1}", fmt, team1, team2,
                             venue_country, mdate, margin=margin, vtype=vtype)

    t1_players = random.sample(country_players[team1], min(3, len(country_players[team1])))
    t2_players = random.sample(country_players[team2], min(3, len(country_players[team2])))

    for pos, player in enumerate(t1_players, start=1):
        runs = random.randint(0, 110)
        balls = max(runs, random.randint(5, 90))
        insert_batting(match_id, player, 1, pos, runs, balls, random.randint(0, 8), random.randint(0, 4))

    for pos, player in enumerate(t2_players, start=1):
        runs = random.randint(0, 110)
        balls = max(runs, random.randint(5, 90))
        insert_batting(match_id, player, 2, pos, runs, balls, random.randint(0, 8), random.randint(0, 4))

    # A couple of bowlers per side
    for player in random.sample(country_players[team2], min(2, len(country_players[team2]))):
        overs = random.randint(4, 10)
        insert_bowling(match_id, player, 1, overs, random.randint(15, 60), random.randint(0, 4))
    for player in random.sample(country_players[team1], min(2, len(country_players[team1]))):
        overs = random.randint(4, 10)
        insert_bowling(match_id, player, 2, overs, random.randint(15, 60), random.randint(0, 4))

    if random.random() < 0.3:
        fielder = random.choice(t1_players + t2_players)
        insert_fielding(match_id, fielder, random.randint(0, 2), random.randint(0, 1), random.randint(0, 1))

conn.commit()

cursor.close()
conn.close()
print("Done! Seed data generated successfully.")