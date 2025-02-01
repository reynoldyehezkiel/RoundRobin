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

connector.c.execute(query_all)
all_data = connector.c.fetchall()

connector.c.execute(query_remain)
remain_data = connector.c.fetchall()