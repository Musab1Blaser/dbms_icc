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

-- Initialise ICC Manager Credentials --
INSERT INTO Power_Users (username, encrypted_password)
VALUES ('ICC_Manager', '2f88ca900ab8fc37d40db0565e0d17763fbd526090c4c4a140a06e153e3789f0');