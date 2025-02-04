from singleton import connect_database as connector

c = connector.db.cursor()

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