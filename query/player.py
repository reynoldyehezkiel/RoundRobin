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

def get_player_teams(pid):
    query = """
        SELECT p.id, p.name
        FROM players p
        LEFT JOIN player_teams pt ON p.id = pt.player_id
        WHERE pt.team_id = (%s)
    """
    connector.cur.execute(query, (pid,))
    return connector.cur.fetchall()

def get_players_by_search(name):
    query = """
        SELECT id, name, total_win
        FROM players
        WHERE name LIKE %s
    """
    connector.cur.execute(query, (f"%{name}%",))
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
    if print_type == "leaderboard":
        print("\n========= Leaderboard =========")
        print("-" * 31)
        print(f"{'Rank':<5} {'Player':<19} {'Wins':>5}")
        print("-" * 31)

        rank = 0
        prev_win = None

        for idx, (pid, name, total_win) in enumerate(data, start=1):
            if total_win != prev_win:
                rank = idx  # Update rank only if the number of wins is different
            prev_win = total_win
            print(f"{rank:<5} {name:<16} {total_win:>5}")

        print("-" * 31)
    else:
        # Print Header
        print("-" * 20)

        if print_type == "team":
            print(f"{team_name.center(20)}")
        elif print_type == "search":
            print(f"{'Player':<15} {'Wins'}")
        else:
            print(f"{'No':<3} {'Player':<20}")

        print("-" * 20)

        # Print Data
        if print_type == "rematch":
            for idx, (match_id, p_id, name) in enumerate(data, start=1):
                print(f"{idx:<4}{name:<21}")
        elif print_type == "search":
            for idx, (pid, name, total_win) in enumerate(data, start=1):
                print(f"{name:<15} {total_win}")
        else:
            for idx, (p_id, name) in enumerate(data, start=1):
                print(f"{idx:<4}{name:<21}")

        print("-" * 20)
