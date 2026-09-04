-- ============================================================
-- Cricbuzz LiveStats — Seed Data (MySQL)
-- ============================================================

USE cricbuzz_livestats;

-- ---------- Teams ----------
INSERT INTO teams (team_name, country) VALUES
('India', 'India'),
('Australia', 'Australia'),
('England', 'England'),
('Pakistan', 'Pakistan'),
('South Africa', 'South Africa'),
('New Zealand', 'New Zealand'),
('Sri Lanka', 'Sri Lanka'),
('West Indies', 'West Indies');

-- ---------- Venues ----------
INSERT INTO venues (venue_name, city, country, capacity) VALUES
('Eden Gardens', 'Kolkata', 'India', 68000),
('Melbourne Cricket Ground', 'Melbourne', 'Australia', 100024),
('Lord''s', 'London', 'England', 30000),
('Gaddafi Stadium', 'Lahore', 'Pakistan', 27000),
('Wanderers Stadium', 'Johannesburg', 'South Africa', 34000),
('Eden Park', 'Auckland', 'New Zealand', 50000);

-- ---------- Series ----------
INSERT INTO series (series_name, host_country, match_type, start_date, total_matches) VALUES
('India tour of Australia 2022', 'Australia', 'Mixed', '2022-11-15', 8),
('ICC World Cup 2023', 'India', 'ODI', '2023-10-05', 48),
('The Ashes 2023', 'England', 'Test', '2023-06-16', 5),
('T20 Tri-Series 2024', 'South Africa', 'T20I', '2024-01-10', 6),
('India tour of New Zealand 2025', 'New Zealand', 'Mixed', '2025-02-01', 6),
('World T20 2026', 'West Indies', 'T20I', '2026-06-01', 10);

-- ---------- Players ----------
INSERT INTO players (full_name, country, playing_role, batting_style, bowling_style) VALUES
('Rohan Verma', 'India', 'Batsman', 'Right-hand bat', NULL),
('Arjun Mehta', 'India', 'All-rounder', 'Right-hand bat', 'Right-arm medium'),
('Vikram Nair', 'India', 'Bowler', 'Right-hand bat', 'Right-arm fast'),
('Steven Clarke', 'Australia', 'Batsman', 'Left-hand bat', NULL),
('Mitchell Grant', 'Australia', 'Bowler', 'Right-hand bat', 'Left-arm fast'),
('Joe Bentley', 'England', 'Batsman', 'Right-hand bat', NULL),
('Sam Wood', 'England', 'All-rounder', 'Left-hand bat', 'Right-arm off break'),
('Imran Sheikh', 'Pakistan', 'All-rounder', 'Right-hand bat', 'Left-arm orthodox'),
('Faisal Khan', 'Pakistan', 'Bowler', 'Right-hand bat', 'Right-arm fast'),
('Dean Roberts', 'South Africa', 'Wicket-keeper', 'Right-hand bat', NULL),
('Kane Wilson', 'New Zealand', 'Batsman', 'Left-hand bat', NULL),
('Trent Foster', 'New Zealand', 'Bowler', 'Right-hand bat', 'Right-arm fast-medium');

-- ---------- Matches ----------
-- format ids: teams 1=India 2=Australia 3=England 4=Pakistan 5=South Africa 6=New Zealand
INSERT INTO matches (series_id, match_desc, format, team1_id, team2_id, venue_id, match_date, toss_winner_id, toss_decision, winner_team_id, victory_margin, victory_type) VALUES
(1, '1st ODI', 'ODI', 1, 2, 2, '2022-11-18', 1, 'bat', 1, 34, 'runs'),
(1, '2nd ODI', 'ODI', 1, 2, 2, '2022-11-21', 2, 'bowl', 2, 5, 'wickets'),
(1, '1st Test', 'Test', 1, 2, 2, '2022-12-01', 1, 'bat', 1, 6, 'wickets'),
(2, 'Group Match', 'ODI', 1, 3, 1, '2023-10-08', 1, 'bowl', 1, 40, 'runs'),
(2, 'Semi Final', 'ODI', 1, 6, 1, '2023-11-15', 6, 'bat', 1, 70, 'runs'),
(2, 'Final', 'ODI', 1, 2, 1, '2023-11-19', 2, 'bat', 2, 6, 'wickets'),
(3, '1st Test', 'Test', 3, 2, 3, '2023-06-16', 3, 'bat', 2, 2, 'wickets'),
(3, '2nd Test', 'Test', 3, 2, 3, '2023-06-28', 2, 'bowl', 3, 43, 'runs'),
(4, 'Match 1', 'T20I', 5, 6, 5, '2024-01-12', 5, 'bat', 5, 15, 'runs'),
(4, 'Match 2', 'T20I', 5, 4, 5, '2024-01-14', 4, 'bowl', 4, 8, 'wickets'),
(4, 'Final', 'T20I', 5, 6, 5, '2024-01-18', 6, 'bat', 6, 3, 'wickets'),
(5, '1st T20I', 'T20I', 1, 6, 6, '2025-02-02', 1, 'bat', 1, 22, 'runs'),
(5, '2nd T20I', 'T20I', 1, 6, 6, '2025-02-05', 6, 'bowl', 6, 4, 'wickets'),
(5, '1st ODI', 'ODI', 1, 6, 6, '2025-02-09', 1, 'bowl', 1, 6, 'wickets'),
(6, 'Match 3', 'T20I', 4, 7, 4, '2026-06-05', 4, 'bat', 4, 18, 'runs'),
(6, 'Match 7', 'T20I', 3, 8, 3, '2026-06-09', 8, 'bat', 3, 5, 'wickets'),
(6, 'Semi Final 1', 'T20I', 1, 3, 1, '2026-06-14', 1, 'bowl', 1, 9, 'wickets');

-- ---------- Batting stats ----------
-- match 1: India (team1) batted first
INSERT INTO batting_stats (match_id, player_id, innings_no, batting_position, runs_scored, balls_faced, fours, sixes, strike_rate, dismissal_type) VALUES
(1, 1, 1, 1, 78, 90, 8, 1, 86.67, 'caught'),
(1, 2, 1, 2, 45, 50, 4, 0, 90.00, 'bowled'),
(1, 3, 1, 3, 12, 20, 1, 0, 60.00, 'run out'),
(2, 1, 1, 1, 34, 40, 3, 0, 85.00, 'caught'),
(2, 2, 1, 2, 56, 60, 5, 1, 93.33, 'not out'),
(3, 1, 1, 1, 102, 180, 10, 0, 56.67, 'caught'),
(3, 2, 1, 2, 60, 110, 6, 0, 54.55, 'bowled'),
(4, 1, 1, 1, 89, 95, 9, 2, 93.68, 'caught'),
(4, 2, 1, 2, 30, 35, 2, 1, 85.71, 'bowled'),
(5, 1, 1, 1, 120, 100, 12, 4, 120.00, 'not out'),
(5, 2, 1, 2, 45, 40, 3, 2, 112.50, 'caught'),
(6, 1, 1, 1, 55, 60, 5, 0, 91.67, 'caught'),
(6, 2, 1, 2, 40, 45, 3, 1, 88.89, 'run out'),
(9, 10, 1, 1, 65, 45, 6, 3, 144.44, 'not out'),
(11, 10, 1, 1, 48, 35, 4, 2, 137.14, 'caught'),
(12, 1, 1, 1, 72, 50, 7, 3, 144.00, 'not out'),
(12, 2, 1, 2, 38, 30, 3, 1, 126.67, 'bowled'),
(13, 1, 1, 1, 28, 25, 2, 1, 112.00, 'caught'),
(14, 1, 1, 1, 95, 80, 9, 2, 118.75, 'not out'),
(16, 6, 1, 1, 40, 35, 4, 1, 114.29, 'caught'),
(16, 7, 1, 2, 33, 28, 3, 1, 117.86, 'not out'),
(17, 1, 1, 1, 88, 70, 8, 3, 125.71, 'caught');

-- ---------- Bowling stats ----------
INSERT INTO bowling_stats (match_id, player_id, innings_no, overs_bowled, runs_conceded, wickets_taken, economy_rate) VALUES
(1, 3, 2, 10, 45, 3, 4.50),
(1, 5, 2, 10, 60, 1, 6.00),
(2, 3, 2, 10, 38, 2, 3.80),
(3, 3, 2, 22, 78, 4, 3.55),
(4, 9, 2, 10, 55, 2, 5.50),
(5, 3, 2, 10, 40, 3, 4.00),
(6, 5, 2, 10, 65, 1, 6.50),
(7, 5, 2, 24, 90, 5, 3.75),
(8, 5, 2, 20, 70, 3, 3.50),
(9, 12, 2, 4, 28, 2, 7.00),
(10, 9, 2, 4, 22, 3, 5.50),
(11, 12, 2, 4, 30, 1, 7.50),
(12, 12, 2, 4, 25, 2, 6.25),
(13, 12, 2, 4, 32, 1, 8.00),
(14, 12, 1, 10, 42, 3, 4.20),
(15, 9, 2, 4, 20, 2, 5.00),
(16, 7, 2, 4, 26, 1, 6.50),
(17, 3, 2, 4, 18, 3, 4.50);

-- ---------- Fielding stats ----------
INSERT INTO fielding_stats (match_id, player_id, catches, stumpings, run_outs) VALUES
(1, 2, 2, 0, 0),
(1, 10, 1, 1, 0),
(2, 3, 1, 0, 1),
(3, 2, 2, 0, 0),
(4, 10, 1, 1, 0),
(5, 2, 3, 0, 0),
(6, 3, 1, 0, 0),
(9, 10, 2, 1, 0),
(11, 10, 1, 0, 1),
(12, 2, 2, 0, 0),
(14, 2, 1, 0, 0),
(16, 7, 1, 0, 0),
(17, 2, 2, 0, 1);