from singleton import connect_database as connector
from singleton import players
from singleton import matches

# Get all players name
players_data = players.get_all_data

# print all players
print("-" * 20)
print(f"{'ID':<3} {'Player':<20}")
print("-" * 20)

for pid, name, total_win in players_data:
    print(f"{pid:<4}{name:<21}")

print()

id_input = int(input("Choose player to delete by ID: "))

player_name = players_data[id_input-1][1]

# get list of player id to update total_win
data_players_id = matches.update_total_win(players_data)

connector.c.execute(players.query_delete, (id_input,))
connector.c.executemany(matches.set_total_win, data_players_id)
connector.db.commit()
print(f"\n✅ Player '{player_name}' deleted successfully!\n")

connector.db.close()
