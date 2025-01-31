from singleton import connect_database as connector
from singleton import retrieve_players as players

if not players.data:
    print("\nNo players available. Please add players first.")
else:
    # print all the data returned by the database
    print("\n----------- Leaderboard -----------")
    print(f"{'Rank':<5} {'Player':<20} {'Wins':>5}")
    print("-" * 35)

    # Print the rank, player name, and number of wins in aligned format
    rank = 1
    for name,total_win in players.data:
        print(f"{rank:<6}{name:<21} {str(total_win)+' wins':>5}")
        rank += 1

# finally closing the database connection
connector.db.close()
