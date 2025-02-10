from query import connect_database as connector
from query import players
from query import matches

# remaining match data if winner_id null
remain_matches = matches.get_remain_data

# update total win
players_data = players.get_by_remaining_match
data_total_win = matches.update_total_win(players_data)

if not remain_matches:
    print("\nNo matches available. Generate new matches first.")
else:
    # show menu
    print("1. All matches")
    print("2. Matches by player")
    menu_input = int(input("Choose Menu: "))
    print()

    # All matches
    if menu_input == 1:
        for match in remain_matches:
            match_id = match[0]
            player1_id = match[1]
            player2_id = match[3]
            player1_name = match[2]
            player2_name = match[4]

            matches.match_players(match_id, player1_id, player1_name, player2_id, player2_name)

    # Matches by player
    elif menu_input == 2:
        while True:

            # print all players data
            players.print_players(players_data)
            id_input = int(input("\nChoose player to start match: "))

            player_id = list(zip(*players_data))[0]

            if id_input not in player_id:
                print(f"\n❌ Player is not in the list. Make sure to input the right ID!\n")
            else:
                for match in remain_matches:
                    match_id = match[0]
                    player1_id = match[1]
                    player2_id = match[3]
                    player1_name = match[2]
                    player2_name = match[4]

                    if player1_id == id_input or player2_id == id_input:
                        matches.match_players(match_id, player1_id, player1_name, player2_id, player2_name)
                break

    else:
        print("\n❌ Invalid choice!")

    # Update total win
    connector.c.executemany(matches.set_total_win, data_total_win)
    connector.db.commit()
    print(f"\n✅ All matches recorded")

# finally closing the database connection
connector.db.close()

