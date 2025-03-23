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
        print("⚠️ No new matches to generate. Matches already exist.")

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

        while True:
            # Get updated data
            data_players = get_player_by_remaining_match()

            if not data_players:
                print("\n⚠️ No players available.")
                break

            print("\n=== Choose Player to Start Match ===")
            print_players(data_players)
            print("⚠️ Type 0 to cancel")

            try:
                index_input = int(input("\nChoose player to start match: ").strip())
            except ValueError:
                print("\n❌ Invalid input. Please enter a valid number.\n")
                continue

            if index_input == 0:
                break

            if not (1 <= index_input <= len(data_players)):
                print("\n❌ Invalid selection. Please choose a number from the list!\n")
                continue

            # Get actual player ID and name
            player_id, player_name = data_players[index_input - 1]

            # Start matches for the selected player
            for match in data_remaining_matches:
                match_id, player1_id, player1_name, player2_id, player2_name = match[:5]

                if player_id in (player1_id, player2_id):
                    match_players(match_id, player1_id, player1_name, player2_id, player2_name)
            break
            # Update total win
        update_total_win(data_players)
        print("\n✅ All matches recorded")

        # Get updated remaining matches
        data_remaining_matches = get_remaining_matches_data()

def rematch():
    data_finished_matches = get_finished_matches_data()
    if not data_finished_matches:
        print("\n⚠️ No finished matches available. Please add players first!")
        return

    while True:
        data_first_player = get_player_by_finished_match()
        data_total_win = update_total_win(data_first_player)

        # Show first players
        print("\n====== Rematch ======")
        print_players(data_first_player)
        print("⚠️ Type 0 to back")

        # Get valid first player input
        while True:
            try:
                index_first_input = int(input("\nChoose first player to rematch: ").strip())
                if index_first_input == 0:
                    return  # Back to main menu
                if 1 <= index_first_input <= len(data_first_player):
                    break
                else:
                    print("\n❌ Invalid selection. Choose a number from the list!")
            except ValueError:
                print("\n❌ Invalid input. Please enter a valid number!\n")

        # Get actual first player ID and name
        first_id_input, first_player_name = data_first_player[index_first_input - 1]

        print(f'\nPlayer {first_player_name} selected!')

        while True:
            # Get valid second players
            data_second_player = [
                (match[0], match[3], match[4]) if match[1] == first_id_input else (match[0], match[1], match[2])
                for match in data_finished_matches if first_id_input in (match[1], match[3])
            ]

            if not data_second_player:
                print("\n⚠️ No valid second players found. Returning to menu.")
                break

            # Show second players
            print()
            print_players(data_second_player, "rematch")
            print("⚠️ Type 0 to back")

            # Get valid second player input
            while True:
                try:
                    index_second_input = int(input("\nChoose second player to rematch: ").strip())
                    if index_second_input == 0:
                        break  # Go back to first player selection
                    if 1 <= index_second_input <= len(data_second_player):
                        break
                    else:
                        print("\n❌ Invalid selection. Choose a number from the list!")
                except ValueError:
                    print("\n❌ Invalid input. Please enter a valid number!\n")

            if index_second_input == 0:
                break

            # Get actual second player data (match_id, p_id, player_name)
            rematch_data = data_second_player[index_second_input - 1]
            rematch_id, rematch_p_id, second_player_name = rematch_data  # Unpack the three elements

            if rematch_id is not None and second_player_name is not None:
                # Match players
                match_players(rematch_id, first_id_input, first_player_name, rematch_p_id, second_player_name)

                # Update total wins
                connector.cur.executemany(query_update_total_win, data_total_win)
                connector.commit()

                print("\n✅ All matches recorded")
                return
