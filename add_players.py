from singleton import connect_database as connector
from singleton import players

# we save all the row data to be inserted in a data variable
players_data = []

print("\n--- Add New Players ---")
print("Please enter player names one by one.")
print("Type 'done' when you are finished adding players.\n")

while True:
    # Asking for player name with instructions
    input_player = input("Enter a player name: ").strip()

    if input_player.lower() == "done":
        print("\n✅ Player saved successfully.")
        break

<<<<<<< Updated upstream
    # if player_name in database["players"]:
    #     print(f"\n⚠️ Player '{player_name}' already exists! Please choose a different name.\n")
    if player_name == "":
        print("\n⚠️ Player name cannot be empty. Please try again.\n")
    else:
        players_data.append(player_name)

# convert list to list of tuples
players_data = zip(*[iter(players_data)]*1)

# execute the insert commands for all rows and commit to the database
connector.c.executemany(players.query_insert, players_data)
connector.db.commit()
=======
    if input_player in existing_players:
        print(f"\n⚠️ Player '{input_player}' already exists! Please choose a different name.\n")
    elif input_player == "":
        print("\n⚠️ Player name cannot be empty. Please try again.\n")
    else:
        new_players.append(input_player)
        print(new_players)

        # convert list to list of tuples
        # new_players = zip(*[iter(new_players)]*1)

        # execute the insert commands for all rows and commit to the database
        # connector.c.executemany(players.query_insert, new_players)
        connector.db.commit()
>>>>>>> Stashed changes

# finally closing the database connection
connector.db.close()
