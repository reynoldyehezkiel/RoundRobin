from db.connection import *

def get_all_teams_data():
    query = """
            SELECT id, name FROM teams;
    """
    connector.cur.execute(query)
    return connector.cur.fetchall()

def get_available_teams(pid):
    query = """
        SELECT t.id, t.name
        FROM teams t
        WHERE NOT EXISTS (
            SELECT 1 
            FROM player_teams pt 
            WHERE pt.team_id = t.id AND pt.player_id = (%s)
        );
    """
    connector.cur.execute(query, (pid,))
    return connector.cur.fetchall()

query_insert_team = """
    INSERT INTO teams
        (id, name)
    VALUES
        (%s, %s)
"""

query_insert_player_team = """
    INSERT INTO player_teams
        (player_id, team_id)
    VALUES
        (%s, %s)
"""

def print_teams(data):
    print("-" * 15)
    print(f"{'No':<3} {'Team':<20}")
    print("-" * 15)

    for idx, (t_id, name) in enumerate(data, start=1):
        print(f"{idx:<4}{name:<21}")
    print("-" * 15)