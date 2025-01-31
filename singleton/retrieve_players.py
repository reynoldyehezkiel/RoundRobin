from singleton import connect_database as connector

c = connector.db.cursor()

query = """
    SELECT name, total_win FROM PLAYERS
    ORDER BY total_win DESC;
"""

# execute the select query to fetch all rows
connector.c.execute(query)

# fetch all the data returned by the database
data = connector.c.fetchall()