from singleton import connect_database as connector
from singleton import players

new_players = []
players_data = []

existing_players = players.get_all_data
if existing_players:
    existing_players = list(zip(*existing_players))[1]

print("\n--- Add New Players ---")
print("Please enter player names one by one.")
print("Type 'done' when you are finished adding players.\n")

while True:
    # Asking for player name with instructions
    player_name = input("Enter a player name: ").strip()

    if player_name.lower() == "done":
        print("\n✅ Finished adding players.")
        break

    if player_name in existing_players:
        print(f"\n⚠️ Player '{player_name}' already exists! Please choose a different name.\n")
    elif player_name == "":
        print("\n⚠️ Player name cannot be empty. Please try again.\n")
    else:
        new_players.append(player_name)
        
        # convert list to list of tuples
        players_data = zip(*[iter(new_players)]*1)

# execute the insert commands for all rows and commit to the database
connector.c.executemany(players.query_insert, players_data)
connector.db.commit()

# finally closing the database connection
connector.db.close()
