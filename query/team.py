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

def get_team_players(tid):
    query = """
        SELECT p.id, p.name
        FROM players p
        LEFT JOIN player_teams pt ON p.id = pt.player_id
        WHERE pt.team_id = (%s)
    """
    connector.cur.execute(query, (tid,))
    return connector.cur.fetchall()

def get_teams_by_search(name):
    query = """
        SELECT id, name
        FROM teams
        WHERE name LIKE %s
    """
    connector.cur.execute(query, (f"%{name}%",))
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

query_delete_team = """
    DELETE FROM teams WHERE id=%s
"""

query_rename_team = """
    UPDATE teams
    SET name = %s
    WHERE id = %s;
"""

def print_teams(data, print_type=None):
    # Print Header
    print("-" * 15)

    if print_type == "search":
        print(f"{'Team':<20}")
    else:
        print(f"{'No':<3} {'Team':<20}")

    print("-" * 15)

    # Print Body

    if print_type == "search":
        for idx, (t_id, name) in enumerate(data, start=1):
            print(f"{name:<21}")
    else:
        for idx, (t_id, name) in enumerate(data, start=1):
            print(f"{idx:<4}{name:<21}")


    print("-" * 15)