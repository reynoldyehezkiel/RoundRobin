# Python implementation to insert data into a table in MySQL
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

# insert statement for players
# this statement will enable us to insert multiple rows at once.
players_insert = """
    INSERT INTO players
        (name)
    VALUES
        (%s)
"""

# we save all the row data to be inserted in a data variable
players_data = []

print("\n--- Add New Players ---")
print("Please enter player names one by one.")
print("Type 'done' when you are finished adding players.\n")

while True:
    # Asking for player name with instructions
    player_name = input("Enter a player name: ").strip()

    if player_name.lower() == "done":
        print("\n✅ Finished adding players.")
        break

    # if player_name in database["players"]:
    #     print(f"\n⚠️ Player '{player_name}' already exists! Please choose a different name.\n")
    if player_name == "":
        print("\n⚠️ Player name cannot be empty. Please try again.\n")
    else:
        players_data.append(player_name)

# convert list to list of tuples
players_data = zip(*[iter(players_data)]*1)

# execute the insert commands for all rows and commit to the database
c.executemany(players_insert, players_data)
db.commit()

# finally closing the database connection
db.close()
