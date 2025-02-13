from query.connection import *

def get_all_players_data():
    if not connector.conn.is_connected():
        connector.conn.reconnect()
    query = """
        SELECT id, name FROM PLAYERS;
    """
    connector.cur.execute(query)
    return connector.cur.fetchall()

def get_leaderboard():
    query = """
        SELECT id, name, total_win FROM PLAYERS
        ORDER BY total_win DESC;
    """
    connector.cur.execute(query)
    return connector.cur.fetchall()

def get_player_by_remaining_match():
    query = """
        SELECT p.id, p.name
        FROM players p
        LEFT JOIN matches m
        ON p.id = m.player1_id OR p.id = m.player2_id
        WHERE m.winner_id IS NULL
        GROUP BY p.id;
    """
    connector.cur.execute(query)
    return connector.cur.fetchall()

def get_player_by_finished_match():
    query = """
        SELECT p.id, p.name
        FROM players p
        LEFT JOIN matches m
        ON p.id = m.player1_id OR p.id = m.player2_id
        WHERE m.winner_id IS NOT NULL
        GROUP BY p.id
        ORDER BY p.id;
    """
    connector.cur.execute(query)
    return connector.cur.fetchall()

query_insert_player = """
    INSERT INTO players
        (id, name)
    VALUES
        (%s, %s)
"""

query_delete_player = """
    DELETE FROM players WHERE id=%s
"""

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
