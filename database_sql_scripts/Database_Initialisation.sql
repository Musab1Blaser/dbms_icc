-- Create Countries table
CREATE TABLE Countries (
    country_code NVARCHAR(3) PRIMARY KEY NOT NULL,
    country_name NVARCHAR(255) NOT NULL
);

-- Create Teams table
CREATE TABLE Teams (
    team_id INT PRIMARY KEY IDENTITY(1,1),
    country_code NVARCHAR(3) REFERENCES Countries(country_code),
    category NVARCHAR(255),
    format NVARCHAR(255)
);

-- Create Power_Users table
CREATE TABLE Power_Users (
    username NVARCHAR(255) PRIMARY KEY,
    encrypted_password NVARCHAR(255) NOT NULL,
    team_id INT REFERENCES Teams(team_id)
);

-- Create Players table
CREATE TABLE Players (
    player_id INT PRIMARY KEY IDENTITY(1,1),
    player_name NVARCHAR(255) NOT NULL,
	country_code NVARCHAR(3) REFERENCES Countries(country_code),
    age INT,
    gender CHAR(1),
    role NVARCHAR(255) NOT NULL
);

-- Create Plays_For table
CREATE TABLE Plays_For (
    roll_no INT PRIMARY KEY IDENTITY(1,1),
    player_id INT REFERENCES Players(player_id),
    team_id INT REFERENCES Teams(team_id)
);

-- Create Matches table
CREATE TABLE Matches (
  match_id INT NOT NULL IDENTITY(1,1) PRIMARY KEY,
  date_time datetime,
  venue VARCHAR(255),
  team_1_id INT NOT NULL FOREIGN KEY REFERENCES Teams(team_id),
  team_2_id INT NOT NULL FOREIGN KEY REFERENCES Teams(team_id),
  completed BIT,
  team_1_confirmation BIT,
  team_2_confirmation BIT
);

--Create Match Results table
CREATE TABLE Match_Results (
    match_id INT PRIMARY KEY,
    team_1_score INT,
    team_1_wickets INT,
    team_1_balls_played INT,
    team_2_score INT,
    team_2_wickets INT,
    team_2_balls_played INT,
    FOREIGN KEY (match_id) REFERENCES Matches(match_id)
);

-- Create Player Match Stats
CREATE TABLE Player_Match_Stats (
    match_id INT,
    roll_no INT,
    bat_runs INT,
    bat_balls INT,
    bat_4s INT,
    bat_6s INT,
    bat_was_out BIT,
    balls_bowled INT,
    ball_wickets INT,
    ball_runs_conceded INT,
    PRIMARY KEY (match_id, roll_no),
    FOREIGN KEY (match_id) REFERENCES Matches(match_id),
    FOREIGN KEY (roll_no) REFERENCES Plays_For(roll_no)
);

-- Creates Tournaments table
CREATE TABLE Tournaments (
    tournament_name VARCHAR(255) PRIMARY KEY,
    category NVARCHAR(255),
    format NVARCHAR(255)
);

-- Creates Tournament_Matches table
CREATE TABLE Tournament_Matches (
    match_id INTEGER PRIMARY KEY FOREIGN KEY REFERENCES Matches(match_id),
    tournament_name VARCHAR(255) FOREIGN KEY REFERENCES Tournaments(tournament_name),
    tournament_stage VARCHAR(255)
);

-- Creates Series table
CREATE TABLE Series (
    series_name VARCHAR(255) PRIMARY KEY,
    team_1_id INTEGER FOREIGN KEY REFERENCES Teams(team_id),
    team_2_id INTEGER FOREIGN KEY REFERENCES Teams(team_id),
    total_matches INTEGER
);

-- Creates Series_Matches table
CREATE TABLE Series_Matches (
    match_id INTEGER PRIMARY KEY FOREIGN KEY REFERENCES Matches(match_id),
    series_name VARCHAR(255) FOREIGN KEY REFERENCES Series(series_name)
);

-- Initialise ICC Manager Credentials --
INSERT INTO Power_Users (username, encrypted_password)
VALUES ('ICC_Manager', '2f88ca900ab8fc37d40db0565e0d17763fbd526090c4c4a140a06e153e3789f0');