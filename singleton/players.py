from singleton import connect_database as connector

c = connector.db.cursor()

def print_all_data():
    print("-" * 20)
    print(f"{'ID':<3} {'Player':<20}")
    print("-" * 20)

    for pid, name, total_win in get_all_data:
        print(f"{pid:<4}{name:<21}")

query_all = """
    SELECT id, name, total_win FROM PLAYERS
    ORDER BY total_win DESC;
"""

query_insert = """
    INSERT INTO players
        (name)
    VALUES
        (%s)
"""

query_delete = """
    DELETE FROM players WHERE id=%s
"""

connector.c.execute(query_all)
get_all_data = connector.c.fetchall()