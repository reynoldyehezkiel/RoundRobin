from itertools import combinations

from query.player import *
from query.match import *

def generate_matches():
    data_players = get_all_players_data()

    if not data_players:
        print("\n⚠️ No players available. Please add players first!")
        return

    # Get all existing matches
    data_matches = get_all_matches_data()

    # If there are no existing matches, initialize an empty set
    existing_matches = set()

    if data_matches:
        # Extract player pairs from existing matches
        existing_matches = set(
            tuple(sorted([match[1], match[2]])) for match in data_matches
        )

    # Get player IDs
    player_ids = [player[0] for player in data_players]

    # Generate all possible player combinations
    new_matches = [
        tuple(sorted(match))
        for match in combinations(player_ids, 2)
        if tuple(sorted(match)) not in existing_matches
    ]

    if new_matches:
        # Insert new matches into the database
        connector.cur.executemany(query_insert_match, new_matches)
        connector.commit()

        print("\n=== Generating New Matches ===")
        print(f"{len(new_matches)} new matches generated and added to the database!")
    else:
        print("⚠️ No new matches to generate (matches already exist).")

def start_match():
    data_remaining_matches = get_remaining_matches_data()

    if not data_remaining_matches:
        print("\n⚠️ No matches available. Please add players first!")
        return

    while True:
        print("\n=== Start Match ===")
        print("1. All matches")
        print("2. Matches by player")
        print("0. Back")

        try:
            menu_input = int(input("Select an option: ").strip())
            if menu_input not in [0, 1, 2]:
                raise ValueError
        except ValueError:
            print("\n❌ Invalid choice! Please enter 0, 1, or 2.\n")
            continue

        if menu_input == 0:
            return

        elif menu_input == 1:
            # Get updated data
            data_players = get_player_by_remaining_match()

            # Start all matches
            for match in data_remaining_matches:
                match_id, player1_id, player1_name, player2_id, player2_name = match[:5]
                match_players(match_id, player1_id, player1_name, player2_id, player2_name)

            # Update total win
            update_total_win(data_players)
            print("\n✅ All matches recorded")
            break

        elif menu_input == 2:
            while True:
                # Get updated data
                data_players = get_player_by_remaining_match()

                print()
                print_players(data_players)
                print("⚠️ Type 0 to cancel")

                try:
                    id_input = int(input("\nChoose player to start match: ").strip())
                except ValueError:
                    print("\n❌ Invalid input! Please enter a valid player ID or 0 to go back.\n")
                    continue

                if id_input == 0:
                    break

                # Create a set of valid player IDs for faster lookup
                player_ids = {player[0] for player in data_players}

                if id_input not in player_ids:
                    print("\n❌ Player is not in the list. Make sure to input the right ID!\n")
                    continue

                # Start matches for the selected player
                for match in data_remaining_matches:
                    match_id, player1_id, player1_name, player2_id, player2_name = match[:5]

                    if id_input in (player1_id, player2_id):
                        match_players(match_id, player1_id, player1_name, player2_id, player2_name)

                # Update total win
                update_total_win(data_players)
                print("\n✅ All matches recorded")


def rematch():
    data_finished_matches = get_finished_matches_data()
    if not data_finished_matches:
        print("\n⚠️ No matches available. Please add players first!")
        return

    data_first_player = get_player_by_finished_match()
    data_total_win = update_total_win(data_first_player)


    # Get valid first player input
    list_first_player_id = {player[0]: player[1] for player in data_first_player}
    while True:
        try:
            print("\n====== Rematch ======")
            print_players(data_first_player)

            first_id_input = int(input("\nChoose first player to rematch: ").strip())
            if first_id_input in list_first_player_id:
                break
            else:
                print("\n❌ Player is not in the list. Make sure to input the right ID!")
        except ValueError:
            print("\n❌ Invalid input. Please enter a valid numeric ID!")

    first_player_name = list_first_player_id[first_id_input]

    # Get valid second players
    data_second_player = [
        (match[0], match[3], match[4]) if match[1] == first_id_input else (match[0], match[1], match[2])
        for match in data_finished_matches if first_id_input in (match[1], match[3])
    ]


    # Get valid second player input
    list_second_player_id = {player[1]: (player[0], player[2]) for player in data_second_player}
    while True:
        try:
            print()
            print_rematch_players(data_second_player)

            second_id_input = int(input("\nChoose second player to rematch: ").strip())
            if second_id_input in list_second_player_id:
                break
            else:
                print("\n❌ Player is not in the list. Make sure to input the right ID!")
        except ValueError:
            print("\n❌ Invalid input. Please enter a valid numeric ID!")

    rematch_id, second_player_name = list_second_player_id[second_id_input]

    # Match players
    match_players(rematch_id, first_id_input, first_player_name, second_id_input, second_player_name)

    # Update total wins
    connector.cur.executemany(query_update_total_win, data_total_win)
    connector.commit()

    print("\n✅ All matches recorded")
