from db.connection import *

def get_all_players_data():
    query = """
        SELECT id, name FROM players;
    """
    connector.cur.execute(query)
    return connector.cur.fetchall()

def get_leaderboard():
    query = """
        SELECT id, name, total_win FROM players
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

query_rename_player = """
    UPDATE players
    SET name = %s
    WHERE id = %s;
"""

def print_players(data, print_type=None, team_name=None):
    print("-" * 20)

    if print_type == "team":
        print(f"{team_name.center(20)}")
    else:
        print(f"{'No':<3} {'Player':<20}")

    print("-" * 20)

    if print_type == "rematch":
        for idx, (match_id, p_id, name) in enumerate(data, start=1):
            print(f"{idx:<4}{name:<21}")
    else:
        for idx, (p_id, name) in enumerate(data, start=1):
            print(f"{idx:<4}{name:<21}")

    print("-" * 20)
