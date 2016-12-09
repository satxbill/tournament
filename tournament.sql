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
DROP DATABASE IF EXISTS tournament;
CREATE DATABASE tournament;
\c tournament
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
-- creates a view listing the player_id, name and total wins sorted by wins in descending order
-- 
DROP VIEW IF EXISTS v_wins;
DROP VIEW IF EXISTS v_losses;

CREATE VIEW v_wins AS
  SELECT players.player_id, count(matches.winner) as wins
    from players left join matches on players.player_id = matches.winner
    group by players.player_id
    order by wins desc;

CREATE VIEW v_losses AS
  SELECT players.player_id, count(matches.loser) as losses
    from players left join matches on players.player_id = matches.loser
    group by players.player_id
    order by losses;
