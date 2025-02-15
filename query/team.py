from db.connection import *

def get_all_teams_data():
    query = """
            SELECT id, name FROM teams;
        """
    connector.cur.execute(query)
    return connector.cur.fetchall()

query_insert_team = """
    INSERT INTO teams
        (id, name)
    VALUES
        (%s, %s)
"""