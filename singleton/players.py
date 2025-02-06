from singleton import connect_database as connector

c = connector.db.cursor()

def print_data(data):
    print("-" * 20)
    print(f"{'ID':<3} {'Player':<20}")
    print("-" * 20)

    for pid, name, total_win in data:
        print(f"{pid:<4}{name:<21}")
    print("-" * 20)

query_all = """
    SELECT id, name, total_win FROM PLAYERS;
"""
connector.c.execute(query_all)
get_all_data = connector.c.fetchall()

query_by_remaining_matches = """
    SELECT p.id, p.name, p.total_win
    FROM players p
    LEFT JOIN matches m ON p.id = m.player1_id
    WHERE m.winner_id IS NULL;
"""
connector.c.execute(query_by_remaining_matches)
get_by_remaining_match = connector.c.fetchall()

query_insert = """
    INSERT INTO players
        (name)
    VALUES
        (%s)
"""

query_delete = """
    DELETE FROM players WHERE id=%s
"""

