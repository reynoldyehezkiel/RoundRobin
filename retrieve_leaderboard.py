# Python implementation to fetch data from a table in MySQL
from xml.etree.ElementTree import tostring

import mysql.connector

# connecting to the mysql server
db = mysql.connector.connect(
	host="localhost",
	user="root",
	passwd="",
	database="roundrobin"
)

# cursor object c
c = db.cursor()

# select statement for tblemployee which returns all columns
players_select = """
    SELECT name, total_win FROM PLAYERS
    ORDER BY total_win DESC;
"""

# execute the select query to fetch all rows
c.execute(players_select)

# fetch all the data returned by the database
employee_data = c.fetchall()

# print all the data returned by the database
print("\n----------- Leaderboard -----------")
print(f"{'Rank':<5} {'Player':<20} {'Wins':>5}")
print("-" * 35)  # Separator line

rank = 1
for name,total_win in employee_data:
    # Print the rank, player name, and number of wins in aligned format
    print(f"{rank:<6}{name:<21} {str(total_win)+' wins':>5}")
    rank += 1

# finally closing the database connection
db.close()
