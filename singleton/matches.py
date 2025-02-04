from singleton import connect_database as connector

c = connector.db.cursor()

query_all = """
    SELECT * FROM MATCHES;
"""

query_remain = """
    SELECT
        m.id,
        m.player1_id, p1.name AS player1_name,
        m.player2_id, p2.name AS player2_name, 
        m.winner_id, p_win.name AS winner_name
    FROM matches m
    LEFT JOIN players p1 ON m.player1_id = p1.id
    LEFT JOIN players p2 ON m.player2_id = p2.id
    LEFT JOIN players p_win ON m.winner_id = p_win.id
    WHERE m.winner_id IS NULL;
"""

query_insert = """
    INSERT INTO matches
        (player1_id, player2_id)
    VALUES
        (%s, %s)
"""

set_winner = """
    UPDATE matches
    SET winner_id = %s
    WHERE id = %s
"""

set_total_win = """
    UPDATE players
    SET total_win = (
      SELECT COUNT(*)
      FROM matches
      WHERE winner_id = %s
    );
"""
# UPDATE players
# SET total_win = total_win + 1
# WHERE id = %s

connector.c.execute(query_all)
get_all_data = connector.c.fetchall()

connector.c.execute(query_remain)
get_remain_data = connector.c.fetchall()
