from query.connection import *

# All Matches
def get_all_matches_data():
    query = """
            SELECT * FROM MATCHES;
        """
    connector.cur.execute(query)
    return connector.cur.fetchall()

# All remain matches
def get_remain_matches_data():
    query = """
        SELECT
            m.id AS match_id,
            m.player1_id, p1.name AS player1_name,
            m.player2_id, p2.name AS player2_name,
            m.winner_id, p_win.name AS winner_name,
            p1.total_win AS player1_total_win
        FROM matches m
        LEFT JOIN players p1 ON m.player1_id = p1.id
        LEFT JOIN players p2 ON m.player2_id = p2.id
        LEFT JOIN players p_win ON m.winner_id = p_win.id
        WHERE m.winner_id IS NULL
        ORDER BY player1_total_win DESC;
    """
    connector.cur.execute(query)
    return connector.cur.fetchall()

# All finished matches
def get_finished_matches_data():
    query = """
        SELECT
            m.id AS match_id,
            m.player1_id, p1.name AS player1_name,
            m.player2_id, p2.name AS player2_name,
            m.winner_id, p_win.name AS winner_name
        FROM matches m
        LEFT JOIN players p1 ON m.player1_id = p1.id
        LEFT JOIN players p2 ON m.player2_id = p2.id
        LEFT JOIN players p_win ON m.winner_id = p_win.id
        WHERE winner_id IS NOT NULL;
        """
    connector.cur.execute(query)
    return connector.cur.fetchall()

# Insert matches data
query_insert_match = """
    INSERT INTO matches
        (player1_id, player2_id)
    VALUES
        (%s, %s)
"""

# Update winner
set_winner = """
    UPDATE matches
    SET winner_id = %s
    WHERE id = %s
"""

# Update total win
set_total_win = """
    UPDATE players
    SET total_win = (
      SELECT COUNT(*)
      FROM matches
      WHERE winner_id = %s
    )
    WHERE id = %s;
"""
