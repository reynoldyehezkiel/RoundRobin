from query import connect_database as connector

query_all = """
    SELECT id, name FROM PLAYERS;
"""
connector.c.execute(query_all)
get_all_player_data = connector.c.fetchall()

query_by_win = """
    SELECT id, name, total_win FROM PLAYERS
    ORDER BY total_win DESC;
"""
connector.c.execute(query_by_win)
get_leaderboard = connector.c.fetchall()

query_by_remaining_matches = """
    SELECT p.id, p.name
    FROM players p
    LEFT JOIN matches m
    ON p.id = m.player1_id OR p.id = m.player2_id
    WHERE m.winner_id IS NULL
    GROUP BY p.id;
"""
connector.c.execute(query_by_remaining_matches)
get_player_by_remaining_match = connector.c.fetchall()

query_by_finished_matches = """
    SELECT p.id, p.name
    FROM players p
    LEFT JOIN matches m
    ON p.id = m.player1_id OR p.id = m.player2_id
    WHERE m.winner_id IS NOT NULL
    GROUP BY p.id
    ORDER BY p.id;
"""
connector.c.execute(query_by_finished_matches)
get_player_by_finished_match = connector.c.fetchall()

query_insert_player = """
    INSERT INTO players
        (name)
    VALUES
        (%s)
"""

query_delete_player = """
    DELETE FROM players WHERE id=%s
"""

