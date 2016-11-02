-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

--
-- SQL to create the database and database tables
--
CREATE DATABASE tournament;
--
-- once the database is created remember to connect to the newly created database before running
-- the SQL to create or drop tables
--
--
-- SQL to drop the players, matches and standings tables (if necessary, skip if first time setting up the db)
--
DROP TABLE players CASCADES;
DROP TABLE matches;
DROP TABLE standings;
--
-- ===================================================================================
-- SQL to create the 'players' table
--
--   Column   |  Type   |                          Modifiers                          
-- -----------+---------+-------------------------------------------------------------
--  player_id | integer | not null default nextval('players_player_id_seq'::regclass)
--  name      | text    | 
--
-- Indexes:
--     "players_pkey" PRIMARY KEY, btree (player_id)
--
CREATE TABLE players (player_id serial primary key, name text);
--
-- ===================================================================================
-- SQL to create the 'matches' table
--
--   Column  |  Type   |                         Modifiers                          
-- ----------+---------+------------------------------------------------------------
--  match_id | integer | not null default nextval('matches_match_id_seq'::regclass)
--  winner   | integer | 
--  loser    | integer | 
--
-- Indexes:
--     "matches_pkey" PRIMARY KEY, btree (match_id)
-- Foreign-key constraints:
--     "matches_loser_fkey" FOREIGN KEY (loser) REFERENCES players(player_id)
--     "matches_winner_fkey" FOREIGN KEY (winner) REFERENCES players(player_id)
--
-- ===================================================================================
--
CREATE TABLE 
    matches (match_id serial primary key, 
    winner int references players (player_id), 
    loser int references players(player_id)
);
--
-- SQL to create the standings table - has player ID, matches won, total matches played
--
--    Column    |  Type   | Modifiers 
-- -------------+---------+-----------
--  player_id   | integer | not null
--  wins        | integer | 
--  num_matches | integer | 
--
-- Indexes:
--     "standings_pkey" PRIMARY KEY, btree (player_id)
-- Foreign-key constraints:
--     "standings_player_id_fkey" FOREIGN KEY (player_id) REFERENCES players(player_id)
--
CREATE TABLE
    standings (player_id int primary key references players (player_id),
    wins int,
    num_matches int
);

