from query import connect_database as connector
from query import players
from query import matches

def match_players(match_data, p1_id, p1_name, p2_id, p2_name):
    print(f"\nMatch: {player1_name} vs {player2_name}")
    print("Please enter '1' for player 1 or '2' for player 2.")
    print("Leave blank and press Enter to skip the match.\n")

    while True:
        winner_choice = input(f"Enter your choice (1 for {player1_name} / 2 for {player2_name}): ").strip()
        if winner_choice == "1":
            connector.c.execute(matches.set_winner, (player1_id, match_id))
            print(f"\n✅ Winner: {player1_name}!")
            break

        elif winner_choice == "2":
            connector.c.execute(matches.set_winner, (player2_id, match_id))
            print(f"\n✅ Winner: {player2_name}!")
            break

        elif winner_choice == "":
            print(f"\n⚠️ Match between {player1_name} and {player2_name} skipped.")
            break

        else:
            print("\n❌ Invalid choice! Please enter '1' or '2' to record a winner or leave blank to skip.")

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

            match_players(remain_matches, player1_id, player1_name, player2_id, player2_name)

    # Matches by player
    elif menu_input == 2:
        while True:

            # print all players data
            players.print_data(players_data)
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
                        match_players(remain_matches, player1_id, player1_name, player2_id, player2_name)
                break

    else:
        print("\n❌ Invalid choice!")

    connector.c.executemany(matches.set_total_win, data_total_win)
    connector.db.commit()
    print(f"\n✅ All matches recorded")

# finally closing the database connection
connector.db.close()

