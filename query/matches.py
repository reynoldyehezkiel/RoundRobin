from query import connect_database as connector

def match_players(m_id, p1_id, p1_name, p2_id, p2_name):
    print(f"\nMatch: {p1_name} vs {p2_name}")
    print("Please enter '1' for player 1 or '2' for player 2.")
    print("Leave blank and press Enter to skip the match.\n")

    while True:
        winner_choice = input(f"Enter your choice (1 for {p1_name} / 2 for {p2_name}): ").strip()
        if winner_choice == "1":
            connector.c.execute(set_winner, (p1_id, m_id))
            print(f"\n✅ Winner: {p1_name}!")
            break

        elif winner_choice == "2":
            connector.c.execute(set_winner, (p2_id, m_id))
            print(f"\n✅ Winner: {p2_name}!")
            break

        elif winner_choice == "":
            print(f"\n⚠️ Match between {p1_name} and {p2_name} skipped.")
            break

        else:
            print("\n❌ Invalid choice! Please enter '1' or '2' to record a winner or leave blank to skip.")


def update_total_win(players_data):
    player_id = list(zip(*players_data))[0]
    result = []
    for i in range(0, len(player_id)):
        player_id_list = (player_id[i], player_id[i])
        result.append(player_id_list)
    return result

c = connector.db.cursor()

# All Matches
query_all = """
    SELECT * FROM MATCHES;
"""
connector.c.execute(query_all)
get_all_data = connector.c.fetchall()

# All remain matches
query_remain = """
    SELECT
        m.id AS match_id,
        m.player1_id, p1.name AS player1_name,
        m.player2_id, p2.name AS player2_name,
        m.winner_id, p_win.name AS winner_name,
        p1.total_win AS player1_total_win
    FROM matches m
    LEFT JOIN players p1 ON m.player1_id = p1.id
    LEFT JOIN players p2 ON m.player2_id = p2.id
    LEFT JOIN players p_win ON m.winner_id = p_win.id
    WHERE m.winner_id IS NULL
    ORDER BY player1_total_win DESC;
"""
connector.c.execute(query_remain)
get_remain_data = connector.c.fetchall()

# All finished matches
query_finished = """
    SELECT
        m.id AS match_id,
        m.player1_id, p1.name AS player1_name,
        m.player2_id, p2.name AS player2_name,
        m.winner_id, p_win.name AS winner_name
    FROM matches m
    LEFT JOIN players p1 ON m.player1_id = p1.id
    LEFT JOIN players p2 ON m.player2_id = p2.id
    LEFT JOIN players p_win ON m.winner_id = p_win.id
    WHERE winner_id IS NOT NULL;
"""
connector.c.execute(query_finished)
get_finished_data = connector.c.fetchall()

# Insert matches data
query_insert = """
    INSERT INTO matches
        (player1_id, player2_id)
    VALUES
        (%s, %s)
"""

# Update winner
set_winner = """
    UPDATE matches
    SET winner_id = %s
    WHERE id = %s
"""

# Update total win
set_total_win = """
    UPDATE players
    SET total_win = (
      SELECT COUNT(*)
      FROM matches
      WHERE winner_id = %s
    )
    WHERE id = %s;
"""
