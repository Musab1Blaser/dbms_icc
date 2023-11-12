-- Clear all tables if they exist --
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

