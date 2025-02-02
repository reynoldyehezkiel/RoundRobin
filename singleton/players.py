from singleton import connect_database as connector

c = connector.db.cursor()

query_all = """
    SELECT id, name, total_win FROM PLAYERS
    ORDER BY total_win DESC;
"""

# execute the select query to fetch all rows
connector.c.execute(query_all)

# fetch all the data returned by the database
get_all_data = connector.c.fetchall()