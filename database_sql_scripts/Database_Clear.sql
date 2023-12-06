-- Clear all tables if they exist --
IF OBJECT_ID('Series_Matches', 'U') IS NOT NULL
    DROP TABLE Series_Matches;

IF OBJECT_ID('Series', 'U') IS NOT NULL
    DROP TABLE Series;

IF OBJECT_ID('Tournament_Matches', 'U') IS NOT NULL
    DROP TABLE Tournament_Matches;

IF OBJECT_ID('Tournaments', 'U') IS NOT NULL
    DROP TABLE Tournaments;

IF OBJECT_ID('Player_Match_Stats ', 'U') IS NOT NULL
    DROP TABLE Player_Match_Stats;

IF OBJECT_ID('Match_Results', 'U') IS NOT NULL
    DROP TABLE Match_Results;

IF OBJECT_ID('Matches', 'U') IS NOT NULL
    DROP TABLE Matches;

IF OBJECT_ID('Plays_For', 'U') IS NOT NULL
    DROP TABLE Plays_For;

IF OBJECT_ID('Power_Users', 'U') IS NOT NULL
    DROP TABLE Power_Users;

IF OBJECT_ID('Teams', 'U') IS NOT NULL
    DROP TABLE Teams;

IF OBJECT_ID('Players', 'U') IS NOT NULL
    DROP TABLE Players;

IF OBJECT_ID('Countries', 'U') IS NOT NULL
    DROP TABLE Countries;