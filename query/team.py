from db.connection import *

def get_all_teams_data():
    query = """
        SELECT id, name, category FROM teams;
    """
    connector.cur.execute(query)
    return connector.cur.fetchall()

def get_available_teams(pid):
    query = """
        SELECT t.id, t.name, t.category
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
        SELECT id, name, category
        FROM teams
        WHERE name LIKE %s
    """
    connector.cur.execute(query, (f"%{name}%",))
    return connector.cur.fetchall()

query_insert_team = """
    INSERT INTO teams
        (id, name, category)
    VALUES
        (%s, %s, %s)
"""

query_insert_team_no_category = """
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
    if print_type == "search":
        # Print Header
        print("-" * 31)
        print(f"{'Team':<15}{'Category'}")
        print("-" * 31)

        # Print Body
        for idx, (t_id, name, category) in enumerate(data, start=1):
            print(f"{name:<15}{category}")

        print("-" * 31)

    elif print_type == "category":
        # Print Header
        print("-" * 15)
        print(f"{'No':<4}{'Category':<20}")
        print("-" * 15)

        # Print Body
        for idx, (category) in enumerate(data, start=1):
            print(f"{idx:<4}{category:<15}")

        print("-" * 15)

        print(f"{len(data)+1:<4}Create New")

        print("-" * 15)

    else:
        # Print Header
        print("-" * 35)
        print(f"{'No':<4}{'Team':<15}{'Category'}")
        print("-" * 35)

        # Print Body
        for idx, (t_id, name, category) in enumerate(data, start=1):
            print(f"{idx:<4}{name:<15}{category}")

        print("-" * 35)