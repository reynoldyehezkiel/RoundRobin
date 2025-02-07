from query import connect_database as connector
from query import players

players_data = players.get_leaderboard
if not players_data:
    print("\nNo players available. Please add players first.")
else:
    # print all players data
    print("\n--------- Leaderboard ---------")
    print(f"{'Rank':<5} {'Player':<19} {'Wins':>5}")
    print("-" * 31)

    # Print the rank, player name, and number of wins in aligned format
    rank = 1
    for pid, name, total_win in players_data:
        print(f"{rank:<6}{name:<20} {str(total_win)}")
        rank += 1
    print("-" * 31)

# finally closing the database connection
connector.db.close()
