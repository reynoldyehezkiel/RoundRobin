from singleton import connect_database as connector
from singleton import players
from singleton import matches

# Get all players name
players_data = players.get_all_data

existing_players = []

if players_data:
    existing_players = list(zip(*players_data))[0]

while True:
    # print all players data
    players.print_data(players_data)
    id_input = int(input("\nChoose player by ID to delete: "))

    if id_input not in existing_players:
        print(f"\n❌ Player is not in the list. Make sure to input the right ID!\n")
    else:
        player_name = ""
        for i in range(0,len(players_data)):
            if id_input == players_data[i][0]:
                player_name = players_data[i][1]

        # get list of player id to update total_win
        data_players_id = matches.update_total_win(players_data)

        # connector.c.execute(players.query_delete, (id_input,))
        # connector.c.executemany(matches.set_total_win, data_players_id)
        connector.db.commit()
        print(f"\n✅ Player '{player_name}' deleted successfully!")

        connector.db.close()
        break
