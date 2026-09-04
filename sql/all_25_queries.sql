-- ============================================================
-- Cricbuzz LiveStats — All 25 SQL Practice Queries (MySQL)
-- ============================================================

USE cricbuzz_livestats;

-- ---------------- BEGINNER (Q1-Q8) ----------------

-- Q1: Players who represent India
SELECT full_name, playing_role, batting_style, bowling_style
FROM players
WHERE country = 'India';

-- Q2: Matches played in the last 30 days
SELECT m.match_desc, t1.team_name AS team1, t2.team_name AS team2,
       v.venue_name, v.city, m.match_date
FROM matches m
JOIN teams t1 ON m.team1_id = t1.team_id
JOIN teams t2 ON m.team2_id = t2.team_id
JOIN venues v ON m.venue_id = v.venue_id
WHERE m.match_date >= CURDATE() - INTERVAL 30 DAY
ORDER BY m.match_date DESC;

-- Q3: Top 10 ODI run scorers
SELECT p.full_name,
       SUM(b.runs_scored) AS total_runs,
       ROUND(AVG(b.runs_scored), 2) AS batting_average,
       SUM(CASE WHEN b.runs_scored >= 100 THEN 1 ELSE 0 END) AS centuries
FROM batting_stats b
JOIN matches m ON b.match_id = m.match_id
JOIN players p ON b.player_id = p.player_id
WHERE m.format = 'ODI'
GROUP BY p.player_id, p.full_name
ORDER BY total_runs DESC
LIMIT 10;

-- Q4: Venues with capacity > 50,000
SELECT venue_name, city, country, capacity
FROM venues
WHERE capacity > 50000
ORDER BY capacity DESC;

-- Q5: Total wins per team
SELECT t.team_name, COUNT(*) AS total_wins
FROM matches m
JOIN teams t ON m.winner_team_id = t.team_id
GROUP BY t.team_id, t.team_name
ORDER BY total_wins DESC;

-- Q6: Player count by playing role
SELECT playing_role, COUNT(*) AS player_count
FROM players
GROUP BY playing_role;

-- Q7: Highest individual score per format
SELECT m.format, MAX(b.runs_scored) AS highest_score
FROM batting_stats b
JOIN matches m ON b.match_id = m.match_id
GROUP BY m.format;

-- Q8: Series started in 2024
SELECT series_name, host_country, match_type, start_date, total_matches
FROM series
WHERE YEAR(start_date) = 2024;


-- ---------------- INTERMEDIATE (Q9-Q16) ----------------

-- Q9: All-rounders with >1000 runs AND >50 wickets (per format)
WITH batting_agg AS (
    SELECT b.player_id, m.format, SUM(b.runs_scored) AS total_runs
    FROM batting_stats b
    JOIN matches m ON b.match_id = m.match_id
    GROUP BY b.player_id, m.format
),
bowling_agg AS (
    SELECT bo.player_id, m.format, SUM(bo.wickets_taken) AS total_wickets
    FROM bowling_stats bo
    JOIN matches m ON bo.match_id = m.match_id
    GROUP BY bo.player_id, m.format
)
SELECT p.full_name, ba.format, ba.total_runs, bw.total_wickets
FROM batting_agg ba
JOIN bowling_agg bw ON ba.player_id = bw.player_id AND ba.format = bw.format
JOIN players p ON p.player_id = ba.player_id
WHERE ba.total_runs > 1000 AND bw.total_wickets > 50;

-- Q10: Last 20 completed matches
SELECT m.match_desc, t1.team_name AS team1, t2.team_name AS team2,
       tw.team_name AS winner, m.victory_margin, m.victory_type, v.venue_name
FROM matches m
JOIN teams t1 ON m.team1_id = t1.team_id
JOIN teams t2 ON m.team2_id = t2.team_id
LEFT JOIN teams tw ON m.winner_team_id = tw.team_id
JOIN venues v ON m.venue_id = v.venue_id
ORDER BY m.match_date DESC
LIMIT 20;

-- Q11: Cross-format performance (players with >= 2 formats)
SELECT p.full_name,
       SUM(CASE WHEN m.format = 'Test' THEN b.runs_scored ELSE 0 END) AS test_runs,
       SUM(CASE WHEN m.format = 'ODI' THEN b.runs_scored ELSE 0 END) AS odi_runs,
       SUM(CASE WHEN m.format = 'T20I' THEN b.runs_scored ELSE 0 END) AS t20i_runs,
       ROUND(AVG(b.runs_scored), 2) AS overall_avg,
       COUNT(DISTINCT m.format) AS formats_played
FROM batting_stats b
JOIN matches m ON b.match_id = m.match_id
JOIN players p ON b.player_id = p.player_id
GROUP BY p.player_id, p.full_name
HAVING formats_played >= 2;

-- Q12: Home vs away wins per team
-- Assumes a team's "home" country matches the venue's country
SELECT t.team_name,
       SUM(CASE WHEN t.country = v.country AND m.winner_team_id = t.team_id THEN 1 ELSE 0 END) AS home_wins,
       SUM(CASE WHEN t.country <> v.country AND m.winner_team_id = t.team_id THEN 1 ELSE 0 END) AS away_wins
FROM matches m
JOIN teams t ON t.team_id IN (m.team1_id, m.team2_id)
JOIN venues v ON m.venue_id = v.venue_id
GROUP BY t.team_id, t.team_name;

-- Q13: Batting partnerships >= 100 runs (consecutive positions)
SELECT p1.full_name AS batsman1, p2.full_name AS batsman2,
       (b1.runs_scored + b2.runs_scored) AS partnership_runs,
       b1.innings_no
FROM batting_stats b1
JOIN batting_stats b2
     ON b1.match_id = b2.match_id
    AND b1.innings_no = b2.innings_no
    AND b2.batting_position = b1.batting_position + 1
JOIN players p1 ON b1.player_id = p1.player_id
JOIN players p2 ON b2.player_id = p2.player_id
WHERE (b1.runs_scored + b2.runs_scored) >= 100
ORDER BY partnership_runs DESC;

-- Q14: Bowling economy by venue (>= 3 matches at venue, >= 4 overs/match)
SELECT p.full_name, v.venue_name,
       ROUND(AVG(bo.economy_rate), 2) AS avg_economy,
       SUM(bo.wickets_taken) AS total_wickets,
       COUNT(DISTINCT bo.match_id) AS matches_played
FROM bowling_stats bo
JOIN matches m ON bo.match_id = m.match_id
JOIN venues v ON m.venue_id = v.venue_id
JOIN players p ON bo.player_id = p.player_id
WHERE bo.overs_bowled >= 4
GROUP BY p.player_id, p.full_name, v.venue_id, v.venue_name
HAVING matches_played >= 3;

-- Q15: Performance in close matches (<50 runs or <5 wickets margin)
-- Assumes a player's team = the team whose country matches the player's country
SELECT p.full_name,
       ROUND(AVG(b.runs_scored), 2) AS avg_runs_close,
       COUNT(*) AS close_matches_played,
       SUM(CASE WHEN t.team_id = m.winner_team_id THEN 1 ELSE 0 END) AS close_matches_won
FROM batting_stats b
JOIN matches m ON b.match_id = m.match_id
JOIN players p ON b.player_id = p.player_id
JOIN teams t ON t.country = p.country
WHERE (m.victory_type = 'runs' AND m.victory_margin < 50)
   OR (m.victory_type = 'wickets' AND m.victory_margin < 5)
GROUP BY p.player_id, p.full_name;

-- Q16: Yearly batting trend since 2020 (>= 5 matches/year)
SELECT p.full_name, YEAR(m.match_date) AS year,
       ROUND(AVG(b.runs_scored), 2) AS avg_runs,
       ROUND(AVG(b.strike_rate), 2) AS avg_strike_rate,
       COUNT(*) AS matches_played
FROM batting_stats b
JOIN matches m ON b.match_id = m.match_id
JOIN players p ON b.player_id = p.player_id
WHERE m.match_date >= '2020-01-01'
GROUP BY p.player_id, p.full_name, YEAR(m.match_date)
HAVING matches_played >= 5;


-- ---------------- ADVANCED (Q17-Q25) ----------------

-- Q17: Toss advantage analysis
SELECT m.toss_decision,
       COUNT(*) AS total_matches,
       SUM(CASE WHEN m.toss_winner_id = m.winner_team_id THEN 1 ELSE 0 END) AS toss_and_match_winner,
       ROUND(100 * SUM(CASE WHEN m.toss_winner_id = m.winner_team_id THEN 1 ELSE 0 END) / COUNT(*), 2) AS win_pct
FROM matches m
WHERE m.toss_decision IS NOT NULL AND m.winner_team_id IS NOT NULL
GROUP BY m.toss_decision;

-- Q18: Most economical bowlers (ODI/T20, >=10 matches, >=2 overs/match avg)
SELECT p.full_name,
       ROUND(SUM(bo.runs_conceded) / SUM(bo.overs_bowled), 2) AS economy_rate,
       SUM(bo.wickets_taken) AS total_wickets,
       COUNT(DISTINCT bo.match_id) AS matches_played,
       ROUND(AVG(bo.overs_bowled), 2) AS avg_overs_per_match
FROM bowling_stats bo
JOIN matches m ON bo.match_id = m.match_id
JOIN players p ON bo.player_id = p.player_id
WHERE m.format IN ('ODI', 'T20I')
GROUP BY p.player_id, p.full_name
HAVING matches_played >= 10 AND avg_overs_per_match >= 2
ORDER BY economy_rate ASC;

-- Q19: Most consistent batsmen (std dev of runs, >=10 balls faced, since 2022)
SELECT p.full_name,
       ROUND(AVG(b.runs_scored), 2) AS avg_runs,
       ROUND(STDDEV_SAMP(b.runs_scored), 2) AS runs_stddev,
       COUNT(*) AS innings_played
FROM batting_stats b
JOIN matches m ON b.match_id = m.match_id
JOIN players p ON b.player_id = p.player_id
WHERE b.balls_faced >= 10 AND m.match_date >= '2022-01-01'
GROUP BY p.player_id, p.full_name
ORDER BY runs_stddev ASC;

-- Q20: Format-wise match count & batting average (>=20 total matches)
WITH per_format AS (
    SELECT p.player_id, p.full_name, m.format,
           COUNT(DISTINCT b.match_id) AS matches_played,
           ROUND(AVG(b.runs_scored), 2) AS batting_avg
    FROM batting_stats b
    JOIN matches m ON b.match_id = m.match_id
    JOIN players p ON b.player_id = p.player_id
    GROUP BY p.player_id, p.full_name, m.format
),
totals AS (
    SELECT player_id, SUM(matches_played) AS total_matches
    FROM per_format
    GROUP BY player_id
)
SELECT pf.full_name,
       SUM(CASE WHEN pf.format = 'Test' THEN pf.matches_played ELSE 0 END) AS test_matches,
       SUM(CASE WHEN pf.format = 'ODI' THEN pf.matches_played ELSE 0 END) AS odi_matches,
       SUM(CASE WHEN pf.format = 'T20I' THEN pf.matches_played ELSE 0 END) AS t20_matches,
       MAX(CASE WHEN pf.format = 'Test' THEN pf.batting_avg END) AS test_avg,
       MAX(CASE WHEN pf.format = 'ODI' THEN pf.batting_avg END) AS odi_avg,
       MAX(CASE WHEN pf.format = 'T20I' THEN pf.batting_avg END) AS t20_avg
FROM per_format pf
JOIN totals t ON pf.player_id = t.player_id
WHERE t.total_matches >= 20
GROUP BY pf.player_id, pf.full_name;

-- Q21: Weighted performance ranking (batting + bowling + fielding)
WITH batting AS (
    SELECT b.player_id, m.format,
           SUM(b.runs_scored) AS runs_scored,
           AVG(b.runs_scored) AS batting_average,
           AVG(b.strike_rate) AS strike_rate
    FROM batting_stats b
    JOIN matches m ON b.match_id = m.match_id
    GROUP BY b.player_id, m.format
),
bowling AS (
    SELECT bo.player_id, m.format,
           SUM(bo.wickets_taken) AS wickets_taken,
           ROUND(SUM(bo.runs_conceded) / NULLIF(SUM(bo.wickets_taken), 0), 2) AS bowling_average,
           ROUND(AVG(bo.economy_rate), 2) AS economy_rate
    FROM bowling_stats bo
    JOIN matches m ON bo.match_id = m.match_id
    GROUP BY bo.player_id, m.format
),
fielding AS (
    SELECT player_id, SUM(catches) AS catches, SUM(stumpings) AS stumpings
    FROM fielding_stats
    GROUP BY player_id
)
SELECT p.full_name, COALESCE(b.format, bw.format) AS format,
       ROUND(
           (COALESCE(b.runs_scored, 0) * 0.01)
         + (COALESCE(b.batting_average, 0) * 0.5)
         + (COALESCE(b.strike_rate, 0) * 0.3)
         + (COALESCE(bw.wickets_taken, 0) * 2)
         + ((50 - COALESCE(bw.bowling_average, 50)) * 0.5)
         + ((6 - COALESCE(bw.economy_rate, 6)) * 2)
         + (COALESCE(f.catches, 0) * 3)
         + (COALESCE(f.stumpings, 0) * 5)
       , 2) AS total_score
FROM players p
LEFT JOIN batting b ON p.player_id = b.player_id
LEFT JOIN bowling bw ON p.player_id = bw.player_id AND bw.format = b.format
LEFT JOIN fielding f ON p.player_id = f.player_id
WHERE b.format IS NOT NULL OR bw.format IS NOT NULL
ORDER BY total_score DESC;

-- Q22: Head-to-head analysis (>=5 matches between a pair in last 3 years)
WITH h2h AS (
    SELECT m.match_id, m.winner_team_id, m.victory_margin,
           LEAST(m.team1_id, m.team2_id) AS team_a,
           GREATEST(m.team1_id, m.team2_id) AS team_b
    FROM matches m
    WHERE m.match_date >= DATE_SUB(CURDATE(), INTERVAL 3 YEAR)
)
SELECT ta.team_name AS team_a, tb.team_name AS team_b,
       COUNT(*) AS total_matches,
       SUM(CASE WHEN h.winner_team_id = h.team_a THEN 1 ELSE 0 END) AS team_a_wins,
       SUM(CASE WHEN h.winner_team_id = h.team_b THEN 1 ELSE 0 END) AS team_b_wins,
       ROUND(AVG(CASE WHEN h.winner_team_id = h.team_a THEN h.victory_margin END), 2) AS team_a_avg_margin,
       ROUND(AVG(CASE WHEN h.winner_team_id = h.team_b THEN h.victory_margin END), 2) AS team_b_avg_margin,
       ROUND(100 * SUM(CASE WHEN h.winner_team_id = h.team_a THEN 1 ELSE 0 END) / COUNT(*), 2) AS team_a_win_pct,
       ROUND(100 * SUM(CASE WHEN h.winner_team_id = h.team_b THEN 1 ELSE 0 END) / COUNT(*), 2) AS team_b_win_pct
FROM h2h h
JOIN teams ta ON h.team_a = ta.team_id
JOIN teams tb ON h.team_b = tb.team_id
GROUP BY h.team_a, h.team_b
HAVING total_matches >= 5;

-- Q23: Recent form (last 10 innings) with form categorization
WITH ranked AS (
    SELECT b.*, m.match_date,
           ROW_NUMBER() OVER (PARTITION BY b.player_id ORDER BY m.match_date DESC) AS rn
    FROM batting_stats b
    JOIN matches m ON b.match_id = m.match_id
)
SELECT p.full_name,
       ROUND((SELECT AVG(runs_scored) FROM ranked r WHERE r.player_id = p.player_id AND r.rn <= 5), 2) AS avg_last5,
       ROUND((SELECT AVG(runs_scored) FROM ranked r WHERE r.player_id = p.player_id AND r.rn <= 10), 2) AS avg_last10,
       ROUND((SELECT AVG(strike_rate) FROM ranked r WHERE r.player_id = p.player_id AND r.rn <= 10), 2) AS recent_strike_rate,
       (SELECT COUNT(*) FROM ranked r WHERE r.player_id = p.player_id AND r.rn <= 10 AND r.runs_scored > 50) AS scores_above_50,
       ROUND((SELECT STDDEV_SAMP(runs_scored) FROM ranked r WHERE r.player_id = p.player_id AND r.rn <= 10), 2) AS consistency_stddev,
       CASE
           WHEN (SELECT AVG(runs_scored) FROM ranked r WHERE r.player_id = p.player_id AND r.rn <= 5) >= 50 THEN 'Excellent Form'
           WHEN (SELECT AVG(runs_scored) FROM ranked r WHERE r.player_id = p.player_id AND r.rn <= 5) >= 35 THEN 'Good Form'
           WHEN (SELECT AVG(runs_scored) FROM ranked r WHERE r.player_id = p.player_id AND r.rn <= 5) >= 20 THEN 'Average Form'
           ELSE 'Poor Form'
       END AS form_category
FROM players p
WHERE EXISTS (SELECT 1 FROM ranked r WHERE r.player_id = p.player_id);

-- Q24: Best batting partnerships (>=5 partnerships between a pair)
WITH partnerships AS (
    SELECT b1.player_id AS p1_id, b2.player_id AS p2_id,
           (b1.runs_scored + b2.runs_scored) AS partnership_runs
    FROM batting_stats b1
    JOIN batting_stats b2
         ON b1.match_id = b2.match_id
        AND b1.innings_no = b2.innings_no
        AND b2.batting_position = b1.batting_position + 1
)
SELECT p1.full_name AS batsman1, p2.full_name AS batsman2,
       COUNT(*) AS partnerships_count,
       ROUND(AVG(pt.partnership_runs), 2) AS avg_partnership_runs,
       SUM(CASE WHEN pt.partnership_runs > 50 THEN 1 ELSE 0 END) AS partnerships_above_50,
       MAX(pt.partnership_runs) AS highest_partnership,
       ROUND(100 * SUM(CASE WHEN pt.partnership_runs > 50 THEN 1 ELSE 0 END) / COUNT(*), 2) AS success_rate_pct
FROM partnerships pt
JOIN players p1 ON pt.p1_id = p1.player_id
JOIN players p2 ON pt.p2_id = p2.player_id
GROUP BY pt.p1_id, pt.p2_id, p1.full_name, p2.full_name
HAVING partnerships_count >= 5
ORDER BY avg_partnership_runs DESC;

-- Q25: Quarterly performance trend & career trajectory
WITH quarterly AS (
    SELECT b.player_id, YEAR(m.match_date) AS yr, QUARTER(m.match_date) AS qtr,
           AVG(b.runs_scored) AS avg_runs,
           AVG(b.strike_rate) AS avg_sr,
           COUNT(*) AS matches_in_quarter
    FROM batting_stats b
    JOIN matches m ON b.match_id = m.match_id
    GROUP BY b.player_id, YEAR(m.match_date), QUARTER(m.match_date)
    HAVING matches_in_quarter >= 3
),
ranked AS (
    SELECT q.*,
           LAG(avg_runs) OVER (PARTITION BY player_id ORDER BY yr, qtr) AS prev_avg_runs,
           COUNT(*) OVER (PARTITION BY player_id) AS total_quarters
    FROM quarterly q
)
SELECT p.full_name, r.yr, r.qtr,
       ROUND(r.avg_runs, 2) AS avg_runs,
       ROUND(r.avg_sr, 2) AS avg_strike_rate,
       CASE
           WHEN r.prev_avg_runs IS NULL THEN 'N/A'
           WHEN r.avg_runs > r.prev_avg_runs THEN 'Improving'
           WHEN r.avg_runs < r.prev_avg_runs THEN 'Declining'
           ELSE 'Stable'
       END AS trend_vs_prev_quarter
FROM ranked r
JOIN players p ON r.player_id = p.player_id
WHERE r.total_quarters >= 6
ORDER BY p.full_name, r.yr, r.qtr;