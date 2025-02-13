from query.connection import *

# All Matches
def get_all_matches_data():
    query = """
            SELECT * FROM MATCHES;
    """
    connector.cur.execute(query)
    return connector.cur.fetchall()

# All remain matches
def get_remaining_matches_data():
    query = """
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
    connector.cur.execute(query)
    return connector.cur.fetchall()

# All finished matches
def get_finished_matches_data():
    query = """
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
    connector.cur.execute(query)
    return connector.cur.fetchall()

# Insert matches data
query_insert_match = """
    INSERT INTO matches
        (player1_id, player2_id)
    VALUES
        (%s, %s)
"""

# Update winner
query_update_winner = """
    UPDATE matches
    SET winner_id = %s
    WHERE id = %s
"""

# Update total win
query_update_total_win = """
    UPDATE players
    SET total_win = (
      SELECT COUNT(*)
      FROM matches
      WHERE winner_id = %s
    )
    WHERE id = %s;
"""

def match_players(m_id, p1_id, p1_name, p2_id, p2_name):
    print(f"\n⚔️ Match: {p1_name} vs {p2_name}")
    print("⚠️ Leave blank and press Enter to skip the match.\n")

    while True:
        winner_choice = input(f"Enter your choice\n[1] {p1_name} / [2] {p2_name}: ").strip()

        if winner_choice == "1":
            winner_id, winner_name = p1_id, p1_name
        elif winner_choice == "2":
            winner_id, winner_name = p2_id, p2_name
        elif winner_choice == "":
            print(f"\n⚠️ Match between {p1_name} and {p2_name} skipped.")
            return
        else:
            print("\n❌ Invalid choice! Please enter '1' or '2' to record a winner or leave blank to skip.")
            continue

        # Update winner in the database
        connector.cur.execute(query_update_winner, (winner_id, m_id))
        print(f"\n✅ Winner: {winner_name}!")
        break

def update_total_win(players_data):
    # No update needed if the list is empty
    if not players_data:
        return

    # Prepare data for updating total wins
    data_total_win = [(player[0], player[0]) for player in players_data]

    # Execute the update query
    connector.cur.executemany(query_update_total_win, data_total_win)
    connector.commit()
