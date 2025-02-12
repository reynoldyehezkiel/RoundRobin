from itertools import combinations

from query.player import *
from query.match import *

def generate_matches():
    data_players = get_all_players_data()
    if not data_players:
        print("\n⚠️ No players available. Please add players first!")
    else:
        # Get all existing matches
        data_matches = get_all_matches_data()

        # Generate new matches for players that haven't been matched yet
        if not data_matches:
            existing_matches = set()
        else:
            # Separate existing match data to player 1 id and player 2 id
            data_player1 = list(zip(*data_matches))[1]
            data_player2 = list(zip(*data_matches))[2]

            existing_matches = []
            # Reconstruct existing match data to "(player1_id, player2_id)"
            for i in range(0, len(data_matches)):
                match_list = (data_player1[i], data_player2[i])
                existing_matches.append(match_list)

        new_matches = []

        # Get player id
        player_id = list(zip(*data_players))[0]

        # Generate new matches for players that haven't been matched yet
        for match in combinations(player_id, 2):
            match = tuple(sorted(match))
            if match not in existing_matches:
                new_matches.append(match)

        # Add new matches
        if new_matches:
            # execute the insert commands for all rows and commit to the database
            connector.cur.executemany(query_insert_match, new_matches)
            connector.commit()

            print("\n=== Generating New Matches ===")
            print(f"{len(new_matches)} new matches generated and added to the database!")
        else:
            print("⚠️ No new matches to generate (matches already exist).")


def start_match():
    # remaining match data if winner_id null
    data_remaining_matches = get_remaining_matches_data()

    if not data_remaining_matches:
        print("\n⚠️ No matches available. Please add players first!")
    else:
        # Get player data
        data_players = get_player_by_remaining_match()
        data_total_win = update_total_win(data_players)
        
        # show menu
        print("\n=== Start Match ===")
        print("1. All matches")
        print("2. Matches by player")
        menu_input = int(input("Select an option: ").strip())

        # All matches
        if menu_input == 1:
            for match in data_remaining_matches:
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
                print_players(data_players)
                id_input = int(input("\nChoose player to start match: ").strip())

                player_id = list(zip(*data_players))[0]

                if id_input not in player_id:
                    print(f"\n❌ Player is not in the list. Make sure to input the right ID!\n")
                else:
                    for match in data_remaining_matches:
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
        connector.cur.executemany(query_update_total_win, data_total_win)
        connector.commit()

        print(f"\n✅ All matches recorded")


def rematch():
    # get data finished matches and player
    data_finished_matches = get_finished_matches_data()

    if not data_finished_matches:
        print("\n⚠️ No matches available. Please add players first!")
    else:
        data_first_player = get_player_by_finished_match()
        data_total_win = update_total_win(data_first_player)

        while True:
            # print all first players
            print("\n====== Rematch ======")
            print_players(data_first_player)
            first_id_input = int(input("\nChoose first player to rematch: ").strip())

            # Get first player id
            list_first_player_id = list(zip(*data_first_player))[0]

            if first_id_input not in list_first_player_id:
                print(f"\n❌ Player is not in the list. Make sure to input the right ID!\n")
            else:
                # Get first player id & name
                first_player_id = ""
                first_player_name = ""
                for i in range(0, len(data_first_player)):
                    if first_id_input == data_first_player[i][0]:
                        first_player_id = data_first_player[i][0]
                        first_player_name = data_first_player[i][1]

                data_second_player = []

                for match in data_finished_matches:
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
                second_id_input = int(input("\nChoose second player to rematch: ").strip())

                # Get second player id
                list_second_player_id = list(zip(*data_second_player))[0]

                if second_id_input not in list_second_player_id:
                    print(f"\n❌ Player is not in the list. Make sure to input the right ID!\n")
                else:
                    # Get second player id & name
                    rematch_id = ""
                    second_player_id = ""
                    second_player_name = ""
                    for i in range(0, len(data_second_player)):
                        if second_id_input == data_second_player[i][1]:
                            rematch_id = data_second_player[i][0]
                            second_player_id = data_second_player[i][1]
                            second_player_name = data_second_player[i][2]

                    match_players(rematch_id, first_player_id, first_player_name, second_player_id, second_player_name)

                    connector.cur.executemany(query_update_total_win, data_total_win)
                    connector.commit()

                    print(f"\n✅ All matches recorded")
                    break
