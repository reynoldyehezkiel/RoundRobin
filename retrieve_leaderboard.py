import connect_database as connector

# cursor object c
c = connector.db.cursor()

# select statement for tblemployee which returns all columns
players_select = """
    SELECT name, total_win FROM PLAYERS
    ORDER BY total_win DESC;
"""

# execute the select query to fetch all rows
c.execute(players_select)

# fetch all the data returned by the database
employee_data = c.fetchall()

if not employee_data:
    print("\nNo players available. Please add players first.")
else:
    # print all the data returned by the database
    print("\n----------- Leaderboard -----------")
    print(f"{'Rank':<5} {'Player':<20} {'Wins':>5}")
    print("-" * 35)

    # Print the rank, player name, and number of wins in aligned format
    rank = 1
    for name,total_win in employee_data:
        print(f"{rank:<6}{name:<21} {str(total_win)+' wins':>5}")
        rank += 1

# finally closing the database connection
connector.db.close()
