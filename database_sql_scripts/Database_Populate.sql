-- Inserting data into the Countries table
INSERT INTO Countries (country_code, country_name) VALUES
    ('PK', 'Pakistan'),
    ('IN', 'India'),
    ('AU', 'Australia'),
    ('ENG', 'England'),
    ('SA', 'South Africa'),
    ('SL', 'Sri Lanka');

-- Inserting data into the Teams table
INSERT INTO Teams (country_code, category, format) VALUES
    ('PK', 'Mens', 'T20I'),
    ('PK', 'Mens', 'ODI'),
    ('PK', 'Mens', 'Test'),
    ('PK', 'Womens', 'T20I'),
    ('IN', 'Mens', 'ODI'),
    ('IN', 'Mens', 'Test'),
    ('IN', 'Womens', 'T20I'),
    ('AU', 'Mens', 'ODI'),
    ('AU', 'Mens', 'Test'),
    ('ENG', 'Womens', 'T20I'),
    ('SA', 'Womens', 'ODI'),
    ('SL', 'Womens', 'Test');

select * from teams;

select * from power_users;

-- Inserting data into the Power_Users table
INSERT INTO Power_Users (username, encrypted_password, team_id) VALUES
    ('PK_M_T20I', '6ca13d52ca70c883e0f0bb101e425a89e8624de51db2d2392593af6a84118090', 1), -- PK Mens T20I
    ('PK_M_ODI', '6ca13d52ca70c883e0f0bb101e425a89e8624de51db2d2392593af6a84118090', 2), -- PK Mens ODI
    ('PK_M_Test', '6ca13d52ca70c883e0f0bb101e425a89e8624de51db2d2392593af6a84118090', 3), -- PK Mens Test
    ('PK_W_T20I', '6ca13d52ca70c883e0f0bb101e425a89e8624de51db2d2392593af6a84118090', 4), -- PK Womens T20I
    ('IN_M_ODI', '6ca13d52ca70c883e0f0bb101e425a89e8624de51db2d2392593af6a84118090', 5), -- IN Mens ODI
    ('IN_M_Test', '6ca13d52ca70c883e0f0bb101e425a89e8624de51db2d2392593af6a84118090', 6), -- IN Mens Test
    ('IN_W_T20I', '6ca13d52ca70c883e0f0bb101e425a89e8624de51db2d2392593af6a84118090', 7), -- IN Womens T20I
    ('AU_M_ODI', '6ca13d52ca70c883e0f0bb101e425a89e8624de51db2d2392593af6a84118090', 8), -- AU Mens ODI
    ('AU_M_Test', '6ca13d52ca70c883e0f0bb101e425a89e8624de51db2d2392593af6a84118090', 9), -- AU Mens Test
    ('ENG_W_T20I', '6ca13d52ca70c883e0f0bb101e425a89e8624de51db2d2392593af6a84118090', 10), -- ENG Womens T20I
    ('SA_W_ODI', '6ca13d52ca70c883e0f0bb101e425a89e8624de51db2d2392593af6a84118090', 11), -- SA Womens ODI
    ('SL_W_Test', '6ca13d52ca70c883e0f0bb101e425a89e8624de51db2d2392593af6a84118090', 12); -- SL Womens Test

-- Pakistani Male Players
INSERT INTO Players (player_name, country_code, age, gender, role) VALUES
    ('Ali Khan', 'PK', 28, 'M', 'Batsman'),
    ('Ahmed Raza', 'PK', 24, 'M', 'Bowler'),
    ('Usman Akram', 'PK', 27, 'M', 'All-Rounder'),
    ('Fahad Aslam', 'PK', 30, 'M', 'Batsman'),
    ('Adeel Ahmed', 'PK', 25, 'M', 'Bowler'),
    ('Saad Mahmood', 'PK', 29, 'M', 'All-Rounder'),
    ('Zain ul Abideen', 'PK', 26, 'M', 'Batsman'),
    ('Imran Malik', 'PK', 31, 'M', 'Bowler'),
    ('Bilal Haider', 'PK', 23, 'M', 'All-Rounder'),
    ('Noman Iqbal', 'PK', 33, 'M', 'Batsman'),
    ('Kamran Shah', 'PK', 32, 'M', 'Bowler'),
    ('Rizwan Ahmed', 'PK', 30, 'M', 'All-Rounder'),
    ('Qasim Ali', 'PK', 35, 'M', 'Batsman'),
    ('Tariq Masood', 'PK', 28, 'M', 'Bowler'),
    ('Adnan Siddique', 'PK', 29, 'M', 'All-Rounder');

-- Pakistan Males T20I Team
INSERT INTO Plays_For (player_id, team_id) VALUES
    (1, 1),  -- Player1 in Pakistan
    (2, 1),  -- Player2 in Pakistan
    (3, 1),  -- Player3 in Pakistan
    (4, 1),  -- Player4 in Pakistan
    (5, 1),  -- Player5 in Pakistan
    (7, 1),  -- Player7 in Pakistan
    (9, 1),  -- Player9 in Pakistan
    (11, 1), -- Player11 in Pakistan
    (12, 1), -- Player12 in Pakistan
    (13, 1), -- Player13 in Pakistan
    (14, 1), -- Player14 in Pakistan
    (15, 1); -- Player15 in Pakistan

-- Pakistan Males ODI Team
INSERT INTO Plays_For (player_id, team_id) VALUES
    (1, 2),  -- Player1 in Pakistan ODI Team 
    (2, 2),  -- Player2 in Pakistan ODI Team 
    (3, 2),  -- Player3 in Pakistan ODI Team 
    (4, 2),  -- Player4 in Pakistan ODI Team
    (5, 2),  -- Player5 in Pakistan ODI Team 
    (6, 2),  -- Player6 in Pakistan ODI Team 
    (8, 2),  -- Player8 in Pakistan ODI Team 
    (10, 2), -- Player10 in Pakistan ODI Team 
    (12, 2), -- Player12 in Pakistan ODI Team 
    (13, 2), -- Player13 in Pakistan ODI Team 
    (14, 2), -- Player14 in Pakistan ODI Team 
    (15, 2); -- Player15 in Pakistan ODI Team 

-- Pakistani Female Players
INSERT INTO Players (player_name, country_code, age, gender, role) VALUES
    ('Aisha Khan', 'PK', 25, 'F', 'Batsman'),
    ('Sana Ahmed', 'PK', 24, 'F', 'Bowler'),
    ('Fatima Akhtar', 'PK', 27, 'F', 'All-Rounder'),
    ('Zara Malik', 'PK', 30, 'F', 'Batsman'),
    ('Nida Aslam', 'PK', 29, 'F', 'Bowler'),
    ('Hira Mahmood', 'PK', 23, 'F', 'All-Rounder'),
    ('Mehak Abideen', 'PK', 26, 'F', 'Batsman'),
    ('Rukhsar Malik', 'PK', 31, 'F', 'Bowler'),
    ('Farah Haider', 'PK', 22, 'F', 'All-Rounder'),
    ('Sadia Iqbal', 'PK', 33, 'F', 'Batsman'),
    ('Naima Shah', 'PK', 32, 'F', 'Bowler'),
    ('Rabia Ahmed', 'PK', 30, 'F', 'All-Rounder'),
    ('Asma Ali', 'PK', 35, 'F', 'Batsman'),
    ('Tasneem Masood', 'PK', 28, 'F', 'Bowler'),
    ('Nadia Siddique', 'PK', 29, 'F', 'All-Rounder');

-- Pakistan Males T20I Team
INSERT INTO Plays_For (player_id, team_id) VALUES
    (16, 4),  -- Aisha Khan in Pakistan Women T20I Team (Team 5)
    (18, 4),  -- Fatima Akhtar in Pakistan Women T20I Team (Team 5)
    (20, 4),  -- Hira Mahmood in Pakistan Women T20I Team (Team 5)
    (22, 4),  -- Mehak Abideen in Pakistan Women T20I Team (Team 5)
    (24, 4),  -- Farah Haider in Pakistan Women T20I Team (Team 5)
    (26, 4),  -- Rabia Ahmed in Pakistan Women T20I Team (Team 5)
    (27, 4),  -- Asma Ali in Pakistan Women T20I Team (Team 5)
    (28, 4),  -- Tasneem Masood in Pakistan Women T20I Team (Team 5)
    (29, 4),  -- Nadia Siddique in Pakistan Women T20I Team (Team 5)
    (17, 4),  -- Sana Ahmed in Pakistan Women T20I Team (Team 5)
    (19, 4),  -- Nida Aslam in Pakistan Women T20I Team (Team 5)
    (21, 4);  -- Rukhsar Malik in Pakistan Women T20I Team (Team 5)

-- Create 15 Male Players for India
INSERT INTO Players (player_name, country_code, age, gender, role) VALUES
    ('Rahul Sharma', 'IN', 28, 'M', 'Batsman'),
    ('Amit Singh', 'IN', 24, 'M', 'Bowler'),
    ('Rajesh Verma', 'IN', 27, 'M', 'All-Rounder'),
    ('Sandeep Kapoor', 'IN', 30, 'M', 'Batsman'),
    ('Anuj Kumar', 'IN', 29, 'M', 'Bowler'),
    ('Vikram Singh', 'IN', 23, 'M', 'All-Rounder'),
    ('Deepak Yadav', 'IN', 26, 'M', 'Batsman'),
    ('Manish Rawat', 'IN', 31, 'M', 'Bowler'),
    ('Prakash Tiwari', 'IN', 22, 'M', 'All-Rounder'),
    ('Alok Yadav', 'IN', 33, 'M', 'Batsman'),
    ('Nikhil Sharma', 'IN', 32, 'M', 'Bowler'),
    ('Ravi Gupta', 'IN', 30, 'M', 'All-Rounder'),
    ('Sanjay Verma', 'IN', 35, 'M', 'Batsman'),
    ('Vishal Kapoor', 'IN', 28, 'M', 'Bowler'),
    ('Rakesh Singh', 'IN', 29, 'M', 'All-Rounder');

-- Populate ODI Team (Team 6) for Indian Male Players
INSERT INTO Plays_For (player_id, team_id) VALUES
    (32, 5),  -- Rahul Sharma in Indian Men ODI Team (Team 6)
    (34, 5),  -- Sandeep Kapoor in Indian Men ODI Team (Team 6)
    (36, 5),  -- Deepak Yadav in Indian Men ODI Team (Team 6)
    (38, 5),  -- Prakash Tiwari in Indian Men ODI Team (Team 6)
    (40, 5),  -- Alok Yadav in Indian Men ODI Team (Team 6)
    (42, 5),  -- Nikhil Sharma in Indian Men ODI Team (Team 6)
    (43, 5),  -- Ravi Gupta in Indian Men ODI Team (Team 6)
    (44, 5),  -- Sanjay Verma in Indian Men ODI Team (Team 6)
    (45, 5),  -- Vishal Kapoor in Indian Men ODI Team (Team 6)
    (33, 5),  -- Amit Singh in Indian Men ODI Team (Team 6)
    (35, 5),  -- Anuj Kumar in Indian Men ODI Team (Team 6)
    (37, 5);  -- Manish Rawat in Indian Men ODI Team (Team 6)

-- Populate Test Team (Team 7) for Indian Male Players
INSERT INTO Plays_For (player_id, team_id) VALUES
    (34, 6),  -- Sandeep Kapoor in Indian Men Test Team (Team 7)
    (36, 6),  -- Deepak Yadav in Indian Men Test Team (Team 7)
    (38, 6),  -- Prakash Tiwari in Indian Men Test Team (Team 7)
    (40, 6),  -- Alok Yadav in Indian Men Test Team (Team 7)
    (42, 6),  -- Nikhil Sharma in Indian Men Test Team (Team 7)
    (44, 6),  -- Sanjay Verma in Indian Men Test Team (Team 7)
    (45, 6),  -- Vishal Kapoor in Indian Men Test Team (Team 7)
    (32, 6),  -- Rahul Sharma in Indian Men Test Team (Team 7)
    (33, 6),  -- Amit Singh in Indian Men Test Team (Team 7)
    (35, 6),  -- Anuj Kumar in Indian Men Test Team (Team 7)
    (37, 6),  -- Manish Rawat in Indian Men Test Team (Team 7)
    (39, 6);  -- Vikram Singh in Indian Men Test Team (Team 7)

-- Create 15 Female Players for India
INSERT INTO Players (player_name, country_code, age, gender, role) VALUES
    ('Anita Sharma', 'IN', 25, 'F', 'Batsman'),
    ('Priya Yadav', 'IN', 24, 'F', 'Bowler'),
    ('Sakshi Verma', 'IN', 27, 'F', 'All-Rounder'),
    ('Pooja Kapoor', 'IN', 30, 'F', 'Batsman'),
    ('Kavita Singh', 'IN', 29, 'F', 'Bowler'),
    ('Neha Yadav', 'IN', 23, 'F', 'All-Rounder'),
    ('Mansi Verma', 'IN', 26, 'F', 'Batsman'),
    ('Riya Tiwari', 'IN', 31, 'F', 'Bowler'),
    ('Aarti Kapoor', 'IN', 22, 'F', 'All-Rounder'),
    ('Shikha Yadav', 'IN', 33, 'F', 'Batsman'),
    ('Neha Sharma', 'IN', 32, 'F', 'Bowler'),
    ('Ritu Gupta', 'IN', 30, 'F', 'All-Rounder'),
    ('Sonam Verma', 'IN', 35, 'F', 'Batsman'),
    ('Preeti Kapoor', 'IN', 28, 'F', 'Bowler'),
    ('Divya Singh', 'IN', 29, 'F', 'All-Rounder');

-- Populate T20I Team (Team 8) for Indian Female Players
INSERT INTO Plays_For (player_id, team_id) VALUES
    (46, 7),  -- Anita Sharma in Indian Women T20I Team (Team 8)
    (47, 7),  -- Priya Yadav in Indian Women T20I Team (Team 8)
    (48, 7),  -- Sakshi Verma in Indian Women T20I Team (Team 8)
    (49, 7),  -- Pooja Kapoor in Indian Women T20I Team (Team 8)
    (50, 7),  -- Kavita Singh in Indian Women T20I Team (Team 8)
    (51, 7),  -- Neha Yadav in Indian Women T20I Team (Team 8)
    (52, 7),  -- Mansi Verma in Indian Women T20I Team (Team 8)
    (53, 7),  -- Riya Tiwari in Indian Women T20I Team (Team 8)
    (54, 7),  -- Aarti Kapoor in Indian Women T20I Team (Team 8)
    (55, 7),  -- Shikha Yadav in Indian Women T20I Team (Team 8)
    (56, 7),  -- Neha Sharma in Indian Women T20I Team (Team 8)
    (57, 7);  -- Ritu Gupta in Indian Women T20I Team (Team 8)

-- Create 15 Male Players for Australia
INSERT INTO Players (player_name, country_code, age, gender, role) VALUES
    ('Mitchell Johnson', 'AU', 32, 'M', 'Batsman'),
    ('David Warner', 'AU', 28, 'M', 'Bowler'),
    ('Steve Smith', 'AU', 29, 'M', 'All-Rounder'),
    ('Usman Khawaja', 'AU', 31, 'M', 'Batsman'),
    ('Pat Cummins', 'AU', 27, 'M', 'Bowler'),
    ('Glenn Maxwell', 'AU', 30, 'M', 'All-Rounder'),
    ('Aaron Finch', 'AU', 29, 'M', 'Batsman'),
    ('Josh Hazlewood', 'AU', 30, 'M', 'Bowler'),
    ('Mitchell Starc', 'AU', 28, 'M', 'All-Rounder'),
    ('Travis Head', 'AU', 26, 'M', 'Batsman'),
    ('Nathan Lyon', 'AU', 31, 'M', 'Bowler'),
    ('Marcus Stoinis', 'AU', 28, 'M', 'All-Rounder'),
    ('Shaun Marsh', 'AU', 35, 'M', 'Batsman'),
    ('Kane Richardson', 'AU', 29, 'M', 'Bowler'),
    ('Ashton Agar', 'AU', 27, 'M', 'All-Rounder');

-- Populate Test Team (Team 10) for Australian Male Players
INSERT INTO Plays_For (player_id, team_id) VALUES
    (61, 9),  -- Mitchell Johnson in Australian Men Test Team (Team 10)
    (62, 9),  -- David Warner in Australian Men Test Team (Team 10)
    (63, 9),  -- Steve Smith in Australian Men Test Team (Team 10)
    (64, 9),  -- Usman Khawaja in Australian Men Test Team (Team 10)
    (65, 9),  -- Pat Cummins in Australian Men Test Team (Team 10)
    (66, 9),  -- Glenn Maxwell in Australian Men Test Team (Team 10)
    (67, 9),  -- Aaron Finch in Australian Men Test Team (Team 10)
    (68, 9),  -- Josh Hazlewood in Australian Men Test Team (Team 10)
    (69, 9),  -- Mitchell Starc in Australian Men Test Team (Team 10)
    (70, 9),  -- Travis Head in Australian Men Test Team (Team 10)
    (71, 9),  -- Nathan Lyon in Australian Men Test Team (Team 10)
    (72, 9);  -- Marcus Stoinis in Australian Men Test Team (Team 10)

-- Create 12 Matches
INSERT INTO Matches (date_time, venue, team_1_id, team_2_id, completed, team_1_confirmation, team_2_confirmation)
VALUES
    ('2023-01-01 12:00:00', 'Eden Gardens, Kolkata', 3, 6, 1, 1, 1), -- PK Mens Test vs IN Mens Test - Series ~
    ('2023-01-02 13:30:00', 'Melbourne Cricket Ground, Melbourne', 4, 7, 1, 1, 1), -- PK Womens T20I vs IND Womens T20I - Series ~
    ('2023-01-03 15:00:00', 'Wankhede Stadium, Mumbai', 5, 8, 1, 1, 1), -- IN Mens ODI vs AU Mens ODI - Tournament Qualifier *
    ('2023-01-04 14:00:00', 'Adelaide Oval, Adelaide', 3, 6, 0, 1, 1), -- PK Mens Test vs IN Mens Test - Series ~
    ('2023-01-05 12:30:00', 'Old Trafford, Manchester', 3, 6, 0, 1, 0), -- PK Mens Test vs IN Mens Test - Series ~
    ('2023-01-06 16:00:00', 'Newlands, Cape Town', 2, 8, 0, 0, 1), -- PK Mens ODI vs AU Mens ODI - Tournament Qualifier *
    ('2023-01-07 17:30:00', 'Galle International Stadium, Galle', 4, 7, 0, 0, 0), -- PK Womens T20I vs IND Womens T20I - Series ~
    ('2023-01-08 18:00:00', 'Rawalpindi Cricket Stadium, Rawalpindi', 9, 6, 0, 1, 1), -- AU Mens Test vs IN Mens Test - Series ~
    ('2023-01-09 12:45:00', 'The Gabba, Brisbane', 9, 6, 0, 0, 1), -- AU Mens Test vs IN Mens Test - Series ~
    ('2023-01-10 14:15:00', 'R.Premadasa Stadium, Colombo', 9, 6, 0, 1, 1), -- AU Mens Test vs IN Mens Test - Series ~
    ('2023-01-11 16:30:00', 'M.Chinnaswamy Stadium, Bengaluru', 5, 2, 0, 1, 1), -- IN Mens ODI vs PK Mens ODI - Tournament Finals *
	('2023-01-12 19:00:00', 'Sydney Cricket Ground, Sydney', 10, 7, 0, 1, 1), -- ENG Womens T20I vs IN Womens T20I = Tournament Quarter Finals *
    ('2023-01-13 12:15:00', 'Sharjah Cricket Stadium, Sharjah', 10, 4, 0, 0, 0); -- ENG Womens T20I vs PK Womens T20I = Tournament Semi Finals *

-- Populate Series table
INSERT INTO Series (series_name, team_1_id, team_2_id, total_matches)
VALUES
    ('PK vs IN Mens Test 2023', 3, 6, 2),
    ('PK vs IND Womens T20I 2023', 4, 7, 1),
    ('AU vs IN Mens Test 2023', 9, 6, 3);

-- Populate Series_Matches table
INSERT INTO Series_Matches (match_id, series_name)
VALUES
    (1, 'PK vs IN Mens Test 2023'),
    (2, 'PK vs IND Womens T20I 2023'),
    (4, 'PK vs IN Mens Test 2023'),
    (5, 'PK vs IN Mens Test 2023'),
    (7, 'PK vs IND Womens T20I 2023'),
    (8, 'AU vs IN Mens Test 2023'),
    (9, 'AU vs IN Mens Test 2023'),
    (10, 'AU vs IN Mens Test 2023');


-- Populate Tournaments table
INSERT INTO Tournaments (tournament_name, category, format)
VALUES
    ('Mens ODI Cup 2023', 'Mens', 'ODI'),
    ('Womens T20I Cup 2023', 'Womens', 'T20I');

-- Populate Tournament_Matches table
INSERT INTO Tournament_Matches (match_id, tournament_name, tournament_stage)
VALUES
    (3, 'Mens ODI Cup 2023', 'Qualifier'),
    (6, 'Mens ODI Cup 2023', 'Qualifier'),
    (11, 'Mens ODI Cup 2023', 'Finals'),
    (12, 'Womens T20I Cup 2023', 'Quarter Finals'),
    (13, 'Womens T20I Cup 2023', 'Semi Finals');


select * from Matches;
select * from tournament_matches;