CREATE TABLE IF NOT EXISTS Seasons (
    season_id INTEGER PRIMARY KEY AUTOINCREMENT,
    season_title TEXT NOT NULL,
    season_start_date TEXT NOT NULL,
    season_end_date TEXT NULL
);

CREATE TABLE IF NOT EXISTS Teams (
    team_id INTEGER PRIMARY KEY AUTOINCREMENT,
    team_name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS Matches (
    match_id INTEGER PRIMARY KEY AUTOINCREMENT,
    match_date TEXT NOT NULL,
    match_start_time TEXT NOT NULL,
    match_end_time TEXT NULL,
    match_season INTEGER REFERENCES Seasons(season_id),
    team_a_id INTEGER REFERENCES Teams(team_id),
    team_b_id INTEGER REFERENCES Teams(team_id),
    team_a_points INTEGER NULL,
    team_b_points INTEGER NULL
);

CREATE TABLE IF NOT EXISTS Notifications (
    notification_id INTEGER PRIMARY KEY AUTOINCREMENT,
    notification_title TEXT NOT NULL,
    notification_description TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS Match_Players (
    match_player_id INTEGER PRIMARY KEY AUTOINCREMENT,
    match_player INTEGER REFERENCES Players(player_id),
    match_id INTEGER REFERENCES Matches(match_id),
    player_active INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS Players (
    player_id INTEGER PRIMARY KEY AUTOINCREMENT,
    player_name TEXT NOT NULL,
    player_gender TEXT NOT NULL,
    player_team INTEGER REFERENCES Teams(team_id) NULL
);

CREATE TABLE IF NOT EXISTS Substitutions (
    substitution_id INTEGER PRIMARY KEY AUTOINCREMENT,
    substitution_time TEXT NOT NULL,
    substitution_match INTEGER REFERENCES Matches(match_id) NOT NULL,
    substituted_player INTEGER REFERENCES Players(player_id) NOT NULL,
    substituting_player INTEGER REFERENCES Players(player_id) NOT NULL
);

CREATE TABLE IF NOT EXISTS Users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_login TEXT NOT NULL,
    user_password TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS Events (
    event_id INTEGER PRIMARY KEY AUTOINCREMENT,
    match_id INTEGER REFERENCES Matches(match_id) NOT NULL,
    event_player_1 INTEGER REFERENCES Players(player_id) NOT NULL,
    event_player_2 INTEGER REFERENCES Players(player_id) NULL,
    event_type TEXT NOT NULL,
    event_value INTEGER NULL
);
