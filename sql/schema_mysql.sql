-- ============================================================
-- Cricbuzz LiveStats — MySQL Schema
-- ============================================================
CREATE DATABASE IF NOT EXISTS cricbuzz_livestats
    CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE cricbuzz_livestats;

-- ---------- Reference tables ----------

CREATE TABLE teams (
    team_id     INT AUTO_INCREMENT PRIMARY KEY,
    team_name   VARCHAR(100) NOT NULL UNIQUE,
    country     VARCHAR(100) NOT NULL
) ENGINE=InnoDB;

CREATE TABLE venues (
    venue_id    INT AUTO_INCREMENT PRIMARY KEY,
    venue_name  VARCHAR(150) NOT NULL,
    city        VARCHAR(100),
    country     VARCHAR(100) NOT NULL,
    capacity    INT
) ENGINE=InnoDB;

CREATE TABLE series (
    series_id      INT AUTO_INCREMENT PRIMARY KEY,
    series_name    VARCHAR(150) NOT NULL,
    host_country   VARCHAR(100),
    match_type     VARCHAR(20),          -- Test / ODI / T20I / Mixed
    start_date     DATE,
    total_matches  INT
) ENGINE=InnoDB;

CREATE TABLE players (
    player_id      INT AUTO_INCREMENT PRIMARY KEY,
    full_name      VARCHAR(150) NOT NULL,
    country        VARCHAR(100) NOT NULL,
    playing_role   ENUM('Batsman','Bowler','All-rounder','Wicket-keeper'),
    batting_style  VARCHAR(50),          -- Right-hand bat / Left-hand bat
    bowling_style  VARCHAR(50)           -- Right-arm fast, Left-arm orthodox, etc.
) ENGINE=InnoDB;

-- ---------- Matches ----------

CREATE TABLE matches (
    match_id         INT AUTO_INCREMENT PRIMARY KEY,
    series_id        INT,
    match_desc       VARCHAR(100),        -- e.g. "3rd ODI"
    format           ENUM('Test','ODI','T20I') NOT NULL,
    team1_id         INT NOT NULL,
    team2_id         INT NOT NULL,
    venue_id         INT,
    match_date       DATE NOT NULL,
    toss_winner_id   INT,
    toss_decision    ENUM('bat','bowl'),
    winner_team_id   INT,
    victory_margin   INT,                 -- number value of the margin
    victory_type     ENUM('runs','wickets','N/A'),
    CONSTRAINT fk_matches_series  FOREIGN KEY (series_id)      REFERENCES series(series_id),
    CONSTRAINT fk_matches_team1   FOREIGN KEY (team1_id)       REFERENCES teams(team_id),
    CONSTRAINT fk_matches_team2   FOREIGN KEY (team2_id)       REFERENCES teams(team_id),
    CONSTRAINT fk_matches_venue   FOREIGN KEY (venue_id)       REFERENCES venues(venue_id),
    CONSTRAINT fk_matches_toss    FOREIGN KEY (toss_winner_id) REFERENCES teams(team_id),
    CONSTRAINT fk_matches_winner  FOREIGN KEY (winner_team_id) REFERENCES teams(team_id)
) ENGINE=InnoDB;

-- ---------- Innings-level performance ----------
-- One row per player per innings batted. batting_position is what
-- makes partnership queries (Q13, Q24) possible: partners are rows
-- with the same match_id + innings_no and positions differing by 1.

CREATE TABLE batting_stats (
    stat_id          INT AUTO_INCREMENT PRIMARY KEY,
    match_id         INT NOT NULL,
    player_id        INT NOT NULL,
    innings_no       INT NOT NULL,        -- 1 or 2 (or 1-4 for Tests)
    batting_position INT NOT NULL,        -- 1-11
    runs_scored      INT DEFAULT 0,
    balls_faced      INT DEFAULT 0,
    fours            INT DEFAULT 0,
    sixes            INT DEFAULT 0,
    strike_rate      DECIMAL(6,2),        -- can be computed, stored for convenience
    dismissal_type   VARCHAR(50),         -- bowled / caught / run out / not out ...
    CONSTRAINT fk_batting_match  FOREIGN KEY (match_id)  REFERENCES matches(match_id),
    CONSTRAINT fk_batting_player FOREIGN KEY (player_id) REFERENCES players(player_id),
    UNIQUE KEY uq_batting (match_id, innings_no, player_id)
) ENGINE=InnoDB;

-- One row per player per innings bowled.

CREATE TABLE bowling_stats (
    stat_id         INT AUTO_INCREMENT PRIMARY KEY,
    match_id        INT NOT NULL,
    player_id       INT NOT NULL,
    innings_no      INT NOT NULL,
    overs_bowled    DECIMAL(4,1) DEFAULT 0,
    runs_conceded   INT DEFAULT 0,
    wickets_taken   INT DEFAULT 0,
    economy_rate    DECIMAL(5,2),         -- runs_conceded / overs_bowled
    CONSTRAINT fk_bowling_match  FOREIGN KEY (match_id)  REFERENCES matches(match_id),
    CONSTRAINT fk_bowling_player FOREIGN KEY (player_id) REFERENCES players(player_id),
    UNIQUE KEY uq_bowling (match_id, innings_no, player_id)
) ENGINE=InnoDB;

-- One row per player per match for fielding — needed for the
-- combined ranking formula in Q21 (catches, stumpings).

CREATE TABLE fielding_stats (
    stat_id     INT AUTO_INCREMENT PRIMARY KEY,
    match_id    INT NOT NULL,
    player_id   INT NOT NULL,
    catches     INT DEFAULT 0,
    stumpings   INT DEFAULT 0,
    run_outs    INT DEFAULT 0,
    CONSTRAINT fk_fielding_match  FOREIGN KEY (match_id)  REFERENCES matches(match_id),
    CONSTRAINT fk_fielding_player FOREIGN KEY (player_id) REFERENCES players(player_id),
    UNIQUE KEY uq_fielding (match_id, player_id)
) ENGINE=InnoDB;

-- ---------- Indexes for the heavier analytical queries ----------

CREATE INDEX idx_matches_date        ON matches(match_date);
CREATE INDEX idx_matches_format      ON matches(format);
CREATE INDEX idx_batting_player      ON batting_stats(player_id);
CREATE INDEX idx_batting_match_inn   ON batting_stats(match_id, innings_no);
CREATE INDEX idx_bowling_player      ON bowling_stats(player_id);
CREATE INDEX idx_bowling_match_inn   ON bowling_stats(match_id, innings_no);
CREATE INDEX idx_fielding_player     ON fielding_stats(player_id);

SELECT COUNT(*) FROM matches;
SELECT COUNT(*) FROM teams;
SELECT COUNT(*) FROM venues;
SELECT COUNT(*) FROM series;
SELECT COUNT(*) FROM players;
SELECT COUNT(*) FROM batting_stats;
SELECT COUNT(*) FROM bowling_stats;
SELECT COUNT(*) FROM fielding_stats;

SELECT COUNT(*) FROM players;
select * from players;
select * from matches;
SELECT * FROM matches WHERE match_date = '2026-09-06';