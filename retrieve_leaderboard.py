from query import connect_database as connector
from query import players

players_data = players.get_leaderboard
if not players_data:
    print("\nNo players available. Please add players first.")
else:
    # Print the rank, player name, and number of wins in aligned format
    print("\n--------- Leaderboard ---------")
    print(f"{'Rank':<5} {'Player':<19} {'Wins':>5}")
    print("-" * 31)

    rank = 0
    prev_win = None
    for idx, (pid, name, total_win) in enumerate(players_data, start=1):
        if total_win != prev_win:
            rank = idx  # Update rank only if score is different
        prev_win = total_win
        print(f"{rank:<6}{name:<20} {str(total_win)}")
    print("-" * 31)

# finally closing the database connection
connector.db.close()
