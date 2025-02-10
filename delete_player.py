from query import connect_database as connector
from query import players
from query import matches

# Get all players name
players_data = players.get_all_data

# Get id player
player_id = list(zip(*players_data))[0]

while True:

    print("Type player ID to delete")
    print("⚠️ Type 0 to cancel\n")

    # Print all players data
    players.print_players(players_data)
    id_input = int(input("\nChoose player: "))

    if id_input == 0:
        print(f"\nDelete player is cancel. No players are deleted.")
        break
    elif id_input not in player_id:
        print(f"\n❌ Player is not in the list. Make sure to input the right ID!\n")
    else:
        # Get player name
        player_name = ""
        for i in range(0,len(players_data)):
            if id_input == players_data[i][0]:
                player_name = players_data[i][1]

        # update total win
        data_total_win = matches.update_total_win(players_data)

        # connector.c.execute(players.query_delete, (id_input,))
        # connector.c.executemany(matches.set_total_win, data_total_win)
        connector.db.commit()
        print(f"\n✅ Player '{player_name}' deleted successfully!")

        connector.db.close()
        break