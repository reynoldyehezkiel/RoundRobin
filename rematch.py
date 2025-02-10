from query import connect_database as connector
from query import players
from query import matches

# get data finished matches and player
finished_matches = matches.get_finished_data
first_player_data = players.get_by_finished_match
data_total_win = matches.update_total_win(first_player_data)

while True:

    # print all first players
    players.print_players(first_player_data)
    first_id_input = int(input("\nChoose first player to rematch: "))

    # Get first player id
    list_first_player_id = list(zip(*first_player_data))[0]

    # Get first player id & name
    first_player_id = ""
    first_player_name = ""
    for i in range(0, len(first_player_data)):
        if first_id_input == first_player_data[i][0]:
            first_player_id = first_player_data[i][0]
            first_player_name = first_player_data[i][1]

    if first_id_input not in list_first_player_id:
        print(f"\n❌ Player is not in the list. Make sure to input the right ID!\n")
    else:

        data_second_player = []

        for match in finished_matches:
            match_id = match[0]
            player1_id = match[1]
            player2_id = match[3]
            player1_name = match[2]
            player2_name = match[4]

            # Reconstruct second player to '(match id, name)'
            if player1_id == first_id_input and player2_name != first_player_name:
                temp_match = (match_id, player2_id ,player2_name)
                data_second_player.append(temp_match)
            if player2_id == first_id_input and player1_name != first_player_name:
                temp_match = (match_id, player1_id, player1_name)
                data_second_player.append(temp_match)

        # print all second players
        players.print_rematch_players(data_second_player)
        second_id_input = int(input("\nChoose second player to rematch: "))

        # Get list second player id
        list_second_player_id = list(zip(*data_second_player))[0]

        # Get second player id & name
        rematch_id = ""
        second_player_id = ""
        second_player_name = ""
        for i in range(0, len(data_second_player)):
            if second_id_input == data_second_player[i][1]:
                rematch_id = data_second_player[i][0]
                second_player_id = data_second_player[i][1]
                second_player_name = data_second_player[i][2]

        # print(f'{rematch_id}. {first_player_id} {first_player_name} vs {second_player_id} {second_player_name}')

        matches.match_players(rematch_id, first_player_id, first_player_name, second_player_id, second_player_name)

        connector.c.executemany(matches.set_total_win, data_total_win)
        connector.db.commit()
        print(f"\n✅ All matches recorded")

        break
