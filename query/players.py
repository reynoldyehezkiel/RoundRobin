from query import connect_database as connector

c = connector.db.cursor()

def print_players(data):
    print("-" * 20)
    print(f"{'ID':<3} {'Player':<20}")
    print("-" * 20)

    for p_id, name in data:
        print(f"{p_id:<4}{name:<21}")
    print("-" * 20)

def print_rematch_players(data):
    print("-" * 20)
    print(f"{'ID':<3} {'Player':<20}")
    print("-" * 20)

    for m_id, p_id, name in data:
        print(f"{p_id:<4}{name:<21}")
    print("-" * 20)

query_all = """
    SELECT id, name FROM PLAYERS;
"""
connector.c.execute(query_all)
get_all_data = connector.c.fetchall()

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
get_by_remaining_match = connector.c.fetchall()

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
get_by_finished_match = connector.c.fetchall()

query_insert = """
    INSERT INTO players
        (name)
    VALUES
        (%s)
"""

query_delete = """
    DELETE FROM players WHERE id=%s
"""

