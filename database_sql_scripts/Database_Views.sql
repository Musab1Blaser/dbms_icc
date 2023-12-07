CREATE OR ALTER PROCEDURE [Team Ratings]
@category NVARCHAR(255), @format NVARCHAR(255), @country NVARCHAR(255), @year int
AS
with results (team_id, matches_won, matches_played) as
(SELECT team_id, 
(SELECT COUNT(M.match_id) FROM Matches M INNER JOIN Match_Results R ON M.match_id = R.match_id WHERE YEAR(CAST(M.date_time AS DATE)) = @year AND ((M.team_1_id = team_id AND R.team_1_score > R.team_2_score)  OR (team_2_id = team_id AND R.team_2_score > R.team_1_score)) AND (completed = 1 AND completed IS NOT NULL)),
(SELECT 1+COUNT(match_id) FROM Matches WHERE YEAR(CAST(date_time AS DATE)) = @year AND (team_1_id = team_id OR team_2_id = team_id) AND (completed = 1 AND completed IS NOT NULL))
FROM Teams)
SELECT T.team_id, 
CAST(300*CAST(R.matches_won AS FLOAT)/R.matches_played AS INT) AS Rating, 
C.country_name 
FROM Teams T INNER JOIN results R ON T.team_id = R.team_id INNER JOIN Countries C ON T.country_code = C.country_code 
WHERE T.category =  @category AND T.format = @format AND C.country_name like @country
ORDER BY Rating DESC;


CREATE OR ALTER PROCEDURE [Player Ratings]
@category NVARCHAR(255), @format NVARCHAR(255), @role NVARCHAR(255), @name NVARCHAR(255), @country NVARCHAR(255), @year int
AS
with rolls (roll_no) as
(SELECT roll_no FROM Plays_For PF INNER JOIN Teams T ON PF.team_id = T.team_id INNER JOIN Players P ON PF.player_id = P.player_id INNER JOIN Countries C ON C.country_code = T.country_code WHERE T.category = @category AND T.format = @format AND P.role = @role AND P.player_name like @name AND C.country_name like @country),
bat_ball_rating (roll_no, bat_rating, ball_rating) AS
(SELECT R.roll_no, 
(SELECT CAST(10*(CAST(SUM(S.bat_runs) AS FLOAT)/(1+SUM(S.bat_balls)) + 5*CAST(SUM(S.bat_runs) AS FLOAT)/(1+COUNT(S.bat_was_out))) AS INT) FROM Player_Match_Stats S INNER JOIN Matches M ON S.match_id = M.match_id AND YEAR(CAST(M.date_time AS DATE)) = @year WHERE S.roll_no = R.roll_no GROUP BY S.roll_no) AS BattingStats,
(SELECT CAST(50*(1.5 - (CAST(SUM(S.ball_runs_conceded) AS FLOAT)/(1+SUM(S.balls_bowled))) + 20*CAST(SUM(S.ball_wickets) AS FLOAT)/(1+COUNT(S.balls_bowled))) AS INT) FROM Player_Match_Stats S INNER JOIN Matches M ON S.match_id = M.match_id AND YEAR(CAST(M.date_time AS DATE)) = @year WHERE S.roll_no = R.roll_no GROUP BY S.roll_no) AS BowlingStats
FROM rolls R)
SELECT P.player_id, P.player_name,
CASE 
WHEN @role = 'Batsman' THEN R.bat_rating
WHEN @role = 'Bowler' THEN R.ball_rating
WHEN @role = 'All-Rounder' THEN (R.bat_rating + R.ball_rating)/2
END AS rating,
C.country_name, P.age
FROM Players P INNER JOIN Plays_For PF ON P.player_id = PF.player_id
INNER JOIN bat_ball_rating R ON R.roll_no = PF.roll_no
INNER JOIN Countries C ON C.country_code = P.country_code
ORDER BY rating DESC;