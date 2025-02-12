from itertools import combinations

from query.player import *
from query.match import *

def generate_matches():
    players_data = get_all_player_data
    if not players_data:
        print("\nNo players available. Please add players first.")
    else:
        # Get all existing matches
        matches_data = get_all_matches_data

        # Generate new matches for players that haven't been matched yet
        if not matches_data:
            existing_matches = set()
        else:
            # Separate existing match data to player 1 id and player 2 id
            player1_data = list(zip(*matches_data))[1]
            player2_data = list(zip(*matches_data))[2]

            existing_matches = []
            # Reconstruct existing match data to "(player1_id, player2_id)"
            for i in range(0, len(matches_data)):
                match_list = (player1_data[i], player2_data[i])
                existing_matches.append(match_list)

        new_matches = []

        # Get player id
        player_id = list(zip(*players_data))[0]

        # Generate new matches for players that haven't been matched yet
        for match in combinations(player_id, 2):
            match = tuple(sorted(match))
            if match not in existing_matches:
                new_matches.append(match)

        # Add new matches
        if new_matches:
            # execute the insert commands for all rows and commit to the database
            connector.c.executemany(query_insert_match, new_matches)
            connector.db.commit()
            print("\n--- Generating New Matches ---")
            print(f"{len(new_matches)} new matches generated and added to the database!")
        else:
            print("⚠️ No new matches to generate (matches already exist).")

    # finally closing the database connection
    connector.db.close()

def start_match():
    # remaining match data if winner_id null
    remain_matches = get_remain_matches_data

    # update total win
    players_data = get_player_by_remaining_match
    data_total_win = update_total_win(players_data)

    if not remain_matches:
        print("\nNo matches available. Generate new matches first.")
    else:
        # show menu
        print("\n=== Start Match ===")
        print("1. All matches")
        print("2. Matches by player")
        menu_input = int(input("Select an option: "))

        # All matches
        if menu_input == 1:
            for match in remain_matches:
                match_id = match[0]
                player1_id = match[1]
                player2_id = match[3]
                player1_name = match[2]
                player2_name = match[4]

                match_players(match_id, player1_id, player1_name, player2_id, player2_name)

        # Matches by player
        elif menu_input == 2:
            while True:

                # print all players data
                print_players(players_data)
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
                            match_players(match_id, player1_id, player1_name, player2_id, player2_name)
                    break

        else:
            print("\n❌ Invalid choice!")

        # Update total win
        connector.c.executemany(set_total_win, data_total_win)
        connector.db.commit()
        print(f"\n✅ All matches recorded")

    # finally closing the database connection
    connector.db.close()

def rematch():
    # get data finished matches and player
    finished_matches = get_finished_matches_data
    first_player_data = get_player_by_finished_match
    data_total_win = update_total_win(first_player_data)

    while True:
        # print all first players
        print("\n====== Rematch ======")
        print_players(first_player_data)
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
                    temp_match = (match_id, player2_id, player2_name)
                    data_second_player.append(temp_match)
                if player2_id == first_id_input and player1_name != first_player_name:
                    temp_match = (match_id, player1_id, player1_name)
                    data_second_player.append(temp_match)

            # print all second players
            print_rematch_players(data_second_player)
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

            match_players(rematch_id, first_player_id, first_player_name, second_player_id, second_player_name)

            connector.c.executemany(set_total_win, data_total_win)
            connector.db.commit()
            print(f"\n✅ All matches recorded")

            break
