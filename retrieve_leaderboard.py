from singleton import connect_database as connector
from singleton import players

players_data = players.get_all_data
if not players_data:
    print("\nNo players available. Please add players first.")
else:
    # print all players data
    print("\n----------- Leaderboard -----------")
    print(f"{'Rank':<5} {'Player':<20} {'Wins':>5}")
    print("-" * 35)

    # Print the rank, player name, and number of wins in aligned format
    rank = 1
    for pid, name, total_win in players_data:
        print(f"{rank:<6}{name:<21} {str(total_win)}")
        rank += 1
    print("-" * 35)

# finally closing the database connection
connector.db.close()
