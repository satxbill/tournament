#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
import bleach


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
#
# Connect to DB and get cursor
#
    DB = connect()
    c = DB.cursor()
#
# delete all the matches
#
    c.execute("DELETE FROM matches;")
#
# reset standings table so players have zero wins and zero matches
#
#    c.execute("UPDATE standings SET wins = 0, num_matches = 0;")

#
# commit and close DB
#
    DB.commit()
    DB.close()


def deletePlayers():
    """Remove all the player records from the database."""

#
# Connect to DB and get cursor
#
    DB = connect()
    c = DB.cursor()
#
# delete all rows from standings and players
#
#    c.execute("DELETE FROM standings;")
    c.execute("DELETE FROM players;")

#
# commit and close DB
#
    DB.commit()
    DB.close()


def countPlayers():
    """Returns the number of players currently registered."""
    #
    # Connect to DB and get cursor
    #
    DB = connect()
    c = DB.cursor()
#
# count the players (well, count # rows in players table)
#
    c.execute("SELECT COUNT(player_id) AS n from players;")
    row = c.fetchone()
#
# close DB
#
    DB.close()
    return row[0]


def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    #
    # make sure the stuff passed to us in 'name' is safe
    #
    c_name = bleach.clean(name)
    #
    # Connect to DB and get cursor
    #
    DB = connect()
    c = DB.cursor()
    #
    # Insert the new player into the db
    #
    c.execute("INSERT INTO players (name) VALUES (%s)", (c_name,))

    DB.commit()
    DB.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place,
    or a player tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    #
    # Connect to DB and get cursor
    #
    DB = connect()
    c = DB.cursor()
    #
    # get the standings
    #
    c.execute('''SELECT players.player_id,
                    players.name,
                    v_wins.wins,
                    v_losses.losses + v_wins.wins as num_matches
                        FROM players, v_wins, v_losses
                        WHERE (players.player_id = v_wins.player_id) AND
                        (players.player_id = v_losses.player_id)
                    ORDER BY v_wins.wins DESC;''')

    rows = c.fetchall()
    return rows


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    #
    # make sure the stuff passed in is safe
    #
    c_winner = bleach.clean(winner)
    c_loser = bleach.clean(loser)
    #
    # Connect to DB and get cursor
    #
    DB = connect()
    c = DB.cursor()
    #
    # Insert the winner and loser into the matches table
    # the DB will assign a match id for each row
    #
    c.execute("INSERT INTO matches (winner, loser) VALUES (%s, %s)",
              (c_winner, c_loser,))

    #
    # commit and close DB
    #
    DB.commit()
    DB.close()


def swissPairings():
    """Returns a list of pairs of players for the next round of a match.

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player
    adjacent to him or her in the standings.

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    #
    # set up an empty list that we'll populate and return
    #
    pairings = []
    #
    # Connect to DB and get cursor
    #
    DB = connect()
    c = DB.cursor()
    #
    # get what we need from the DB
    #
    c.execute('''SELECT players.player_id,
                    players.name,
                    v_wins.wins
                        FROM players, v_wins
                        WHERE (players.player_id = v_wins.player_id)
                    ORDER BY v_wins.wins DESC;''')
    #
    # let's see what we got from the DB
    #
    rows = c.fetchall()
    #
    # make sure we have an even number of players
    #
    if len(rows) % 2 == 0:
        i = 0
        while i in range(len(rows) - 1):
            #
            # put the pairings together, we sorted by wins in our query so
            # all we need to do is put the ordered results together in pairs:
            #    1 and 2
            #    3 and 4
            #    etc...
            # until all players are paired.
            #
            pairing = (rows[i][0], rows[i][1], rows[i+1][0], rows[i+1][1])
            #
            # append the current pairing to the list of pairings we'll return
            #
            pairings.append(pairing)
            #
            # bump loop index by 2 to get to the next 2 players to be paired
            #
            i = i + 2
    else:
        #
        # oops.. somthing went wrong, we don't have an even number of players
        #
        raise ValueError(
            "Odd number of players {n}".format(n=len(rows)))

    return pairings
