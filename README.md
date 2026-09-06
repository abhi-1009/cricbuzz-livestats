# 🏏 Cricbuzz LiveStats
### Real-Time Cricket Insights & SQL-Based Analytics

![Python](https://img.shields.io/badge/Python-3.12-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-red)
![MySQL](https://img.shields.io/badge/MySQL-Database-4479A1)
![API](https://img.shields.io/badge/Cricbuzz-API-orange)
![GitHub](https://img.shields.io/badge/GitHub-abhi--1009-black)

---

## 📌 Project Overview

**Cricbuzz LiveStats** is an end-to-end cricket analytics platform that combines **live match data from the Cricbuzz API** with a **cloud-hosted MySQL analytics and record-management system**, all delivered through an interactive, custom-themed Streamlit dashboard.

- 🔴 **Live data** — pull live match scores, statuses, and full batting/bowling scorecards directly from the Cricbuzz API
- 🗄️ **Structured analytics** — a purpose-built MySQL schema (teams, players, matches, batting/bowling/fielding stats) answering 25 SQL questions across beginner, intermediate, and advanced difficulty
- 🛠️ **Full CRUD** — create, read, update, and delete player and match records directly from the app, no manual SQL required
- 📈 **Visual insights** — dedicated charts page (team wins, format split, player roles, toss advantage, top scorers)
- 🎨 **Custom theming** — dark UI with a distinct accent color per page

> **Live App:** https://cricbuzz-livestats-4f9rpyqumzwm6zbesbs63d.streamlit.app/

---

## 🧠 Problem Statement

Cricket fans, analysts, and learners often have to switch between multiple sources — a live-score app, a stats website, and a separate database tool — to get a full picture of a match, a player's career, or historical trends. Cricbuzz LiveStats consolidates all three into one dashboard: live match tracking, statistical leaderboards, and a full SQL analytics layer over a relational cricket database, plus the ability to manage that database's records without leaving the app.

**Use Cases:**
- 📺 **Live match tracking** — real-time scores and detailed scorecards without leaving the dashboard
- 📊 **Player performance analysis** — leaderboards and 25 pre-built SQL analyses covering form, consistency, partnerships, and rankings
- 🎓 **SQL learning tool** — a working example of beginner → advanced SQL (joins, subqueries, window functions, CTEs) against a real relational schema
- 🗃️ **Database management practice** — hands-on CRUD operations against a live, cloud-hosted MySQL database via form-based UI

---

## 📂 Project Structure

```
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
│   ├── Live Match.py
│   ├── Top Player Stats.py
│   ├── SQL Analytics.py
│   ├── CRUD Operations.py    
│   ├── Visualizations.py
│   └── Conclusion.py
├── sql/
│   ├── schema_mysql.sql     # Database schema (CREATE TABLE statements)
│   ├── seed_data.sql        # Initial small seed dataset
│   └── all_25_queries.sql   # All 25 SQL queries as standalone reference
└── sample_data/
    ├── recent_matches.json  # Saved API response samples (for offline dev)
    └── scorecard.json

```
---

## 📊 Database Schema

| Table | Description |
|---|---|
| `teams` | International teams and their countries |
| `venues` | Grounds, cities, countries, seating capacity |
| `series` | Bilateral/multi-team series metadata |
| `players` | Player identity, country, role, batting/bowling style |
| `matches` | Match results, toss, venue, victory margin/type |
| `batting_stats` | Per-innings batting figures, including batting position (enables partnership analysis) |
| `bowling_stats` | Per-innings bowling figures (overs, economy, wickets) |
| `fielding_stats` | Catches, stumpings, run-outs per match |

Seed data is generated via `generate_seed_data.py`, engineered so every one of the 25 SQL queries returns meaningful (non-empty) results — e.g. a dedicated all-rounder with 36 matches spanning 12 quarters, and a bilateral series with 5+ head-to-head matches. The database is hosted on **Aiven's free-tier cloud MySQL**, reachable both locally (via MySQL Workbench) and from the deployed Streamlit Cloud app.
---

## 🔧 Project Workflow

### Step 1 — API Integration
Connected to the Cricbuzz Cricket API (via RapidAPI) with a centralized `api_client.py` wrapper handling live matches, recent/upcoming matches, scorecards, and top-stats leaderboards, with error handling and response caching to respect the free-tier rate limit (200 requests/month).

### Step 2 — Database Design
Designed a normalized MySQL schema across 8 tables, purpose-built to support 25 SQL analysis questions — including window functions, CTEs, and multi-table joins.

### Step 3 — SQL Analytics
Wrote and validated all 25 queries directly in MySQL Workbench, then wired them into an in-app query selector with live execution against the database and one-click CSV export of results.

### Step 4 — Streamlit Dashboard
Built a 6-page app: Home, Live Match (with scorecard drill-down), Top Player Stats (with leaderboard chart), SQL Analytics, CRUD Operations, and Visualizations.

### Step 5 — CRUD Layer
Added form-based Create/Read/Update/Delete for both players and matches, with input validation and safe handling of foreign-key constraints.

### Step 6 — Styling & Theming
Applied a consistent dark theme via `.streamlit/config.toml`, plus a shared `utils/styling.py` module giving each page its own accent color and subtly tinted background gradient.

### Step 7 — Cloud Deployment
Migrated the database to Aiven's cloud MySQL (reusing an existing free-tier Aiven organization), refactored credential handling to support both local `.env` and Streamlit Cloud secrets via `utils/config.py`, and deployed the app on Streamlit Community Cloud.

---

## 📱 Streamlit App Pages

| Page | Contents |
|---|---|
| 🏠 Home | Project overview, tools used, usage instructions, folder structure |
| ⚡ Live Match | Live/recent match list + detailed scorecard viewer (batting & bowling per innings) |
| 📊 Top Player Stats | Batting/bowling leaderboards across categories (Most Runs, Most Wickets, Highest Score, etc.), with a leaderboard bar chart |
| 🔍 SQL Analytics | 25 SQL queries across beginner/intermediate/advanced levels, run live against MySQL, with CSV export |
| 🛠️ CRUD Operations | Add/view/edit/delete players and matches via forms |
| 📈 Visualizations | Team wins, match format split, player role distribution, toss-decision win rate, top ODI run scorers |

---

## 🚀 How to Run Locally

**1. Clone the repository:**
```bash
git clone https://github.com/abhi-1009/cricbuzz-livestats.git
cd cricbuzz-livestats
```

**2. Create a virtual environment:**
```bash
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux
```

**3. Install dependencies:**
```bash
pip install -r requirements.txt
```

**4. Set up MySQL:**
- Open MySQL Workbench and run `sql/schema_mysql.sql` against either a local MySQL instance or a cloud instance (e.g. Aiven) — this creates the `cricbuzz_livestats` database and all 8 tables
- Populate it with `python generate_seed_data.py` (recommended — a larger, engineered dataset that satisfies every SQL query's data thresholds) or `sql/seed_data.sql` for a minimal starter set

**5. Configure environment variables:**

Create your own `.env` file in the project root (this file is gitignored — you must create it locally):
```
RAPIDAPI_KEY=your_rapidapi_key_here
RAPIDAPI_HOST=cricbuzz-cricket.p.rapidapi.com
MYSQL_HOST=your_mysql_host_here
MYSQL_PORT=your_mysql_port_here
MYSQL_USER=your_mysql_user_here
MYSQL_PASSWORD=your_mysql_password_here
MYSQL_DATABASE=cricbuzz_livestats
```
Get a free RapidAPI key by subscribing to the **Cricbuzz Cricket API** on [RapidAPI](https://rapidapi.com) (Basic/free plan — 200 requests/month). `MYSQL_HOST`/`PORT`/`USER`/`PASSWORD` point at either a local MySQL server (`localhost`, port `3306`, user `root`) or a cloud instance such as Aiven.

**6. Launch the Streamlit app:**
```bash
streamlit run main.py
```
Opens at `http://localhost:8501`.

> ⚠️ Always launch with `streamlit run home.py` — running it as a plain Python file will not start the web app.
---

## ☁️ Deployment

This app is deployed with a **cloud-hosted MySQL database**, since the SQL Analytics and CRUD pages need live read/write access — a purely local database would make hosted deployment impossible.

1. **Database:** Hosted on [Aiven](https://aiven.io) (free-tier MySQL service). Schema and seed data were loaded by temporarily pointing a local `.env` at the Aiven host and running `generate_seed_data.py` once.
2. **Credential handling:** `utils/config.py` reads config values from `st.secrets` when running on Streamlit Cloud, falling back to local `.env` values otherwise — no code differs between local and deployed environments.
3. **App hosting:** Deployed via [Streamlit Community Cloud](https://share.streamlit.io), connected directly to this GitHub repository.
4. **Secrets:** `RAPIDAPI_KEY`, `RAPIDAPI_HOST`, `MYSQL_HOST`, `MYSQL_PORT`, `MYSQL_USER`, `MYSQL_PASSWORD`, and `MYSQL_DATABASE` are configured as Streamlit Cloud secrets — never committed to the repository.

---

## 📦 Requirements

```
streamlit
requests
pandas
python-dotenv
mysql-connector-python
matplotlib

```

---

## 🛠 Tech Stack

| Category | Tools |
|---|---|
| Language | Python 3.12 |
| Live Data | Cricbuzz Cricket API (via RapidAPI) |
| Database | MySQL 8.0+ (Aiven cloud, mysql-connector-python) |
| Data Handling | Pandas |
| Visualization | Streamlit native charts, Matplotlib |
| Web App | Streamlit (custom theme via config.toml + shared CSS) |
| Version Control | Git + GitHub |
| Deployment | Streamlit Community Cloud |

---

## 📌 Key Highlights

- 🏏 **All 25 SQL questions answered** — from basic filters to window-function-based form/trend analysis and a custom weighted player ranking formula
- 📉 **Real threshold-satisfying data** — seed data specifically engineered so advanced queries (≥20 matches, ≥6 quarters, ≥5 head-to-head matches) return real results, not empty tables
- 🔌 **API-quota aware design** — caching throughout to stay within the free-tier 200 requests/month limit
- 🗃️ **Safe CRUD** — delete operations respect foreign-key integrity and fail gracefully rather than corrupting linked stats
- ☁️ **Fully cloud-deployed** — live MySQL on Aiven + app hosted on Streamlit Community Cloud, with unified local/cloud credential handling
- 📥 **CSV export** on every SQL Analytics query result
- 🎨 **Distinct per-page theming** — each page has its own accent color and tinted background for quick visual orientation

---

## 👨‍💻 Author

**Abhijit Sinha**
[GitHub](https://github.com/abhi-1009)

---

*Cricbuzz LiveStats — Real-Time Cricket Insights & SQL-Based Analytics*