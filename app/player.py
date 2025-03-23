from app.match import generate_matches
from query.player import *
from query.match import *
from query.team import *

def add_players():
    # Get existing players from the database
    data_players = get_all_players_data()
    existing_players = set(name for _, name in data_players) if data_players else set()

    print("\n=== Add New Players ===")
    print("Please enter player names one by one.")
    print("⚠️ Press Enter to finish adding players.")
    print("⚠️ Type 0 to back\n")

    new_players = []  # List to store newly added players

    while True:
        # Asking for player name
        name_input = input("Enter a player name: ").strip()

        # If the user presses enter, commit the database changes
        if name_input == "":
            if new_players:
                # Commit new players to the database
                connector.cur.executemany(query_insert_player, new_players)
                connector.commit()
                print(f"\n✅ Finished adding {len(new_players)} players.")

                # Generate matches after adding players
                generate_matches()
                break
            else:
                print("\n⚠️ Player's name can't be empty!\n")

        # Cancel operation
        elif name_input == "0":
            break

        # Validate player name
        elif name_input in existing_players:
            print(f"\n⚠️ Player '{name_input}' already exists! Please choose a different name.\n")
        else:
            # Add new player to the list
            new_players.append((None, name_input))
            existing_players.add(name_input)

def view_leaderboard():
    data_players = get_leaderboard()

    if not data_players:
        print("\n⚠️ No players available. Please add players first!")
        return

    print_players(data_players, "leaderboard")

def search_players():
    print()
    search_input = input("Enter player name to search: ").strip()
    player_name = get_players_by_search(search_input)
    print()

    if player_name:
        print_players(player_name, "search")
    else:
        print("No players found.")

def rename_player():
    # Get existing players from the database
    data_players = get_all_players_data()
    existing_players = set(name for _, name in data_players) if data_players else set()

    if not data_players:
        print("\n⚠️ No players available. Please add players first!")
        return

    while True:
        print("\n=== Rename Player ===")
        print_players(data_players)
        print("⚠️ Type 0 to back")

        try:
            index_input = int(input("\nChoose player to rename: ").strip())
        except ValueError:
            print("\n❌ Invalid input! Please enter a valid number.")
            continue

        if index_input == 0:
            break
        elif not (1 <= index_input <= len(data_players)):
            print("\n❌ Invalid selection. Please choose a number from the list!")
        else:
            # Get actual player ID and name
            player_id, player_name = data_players[index_input - 1]

            print(f"\n✅ Player '{player_name}' selected!")
            print("⚠️ Type 0 to back")

            while True:
                new_name_input = input("\nEnter new player name: ").strip()

                if new_name_input == player_name:
                    print("\n⚠️ Player's name can't be same!")

                elif new_name_input == "":
                    print("\n⚠️ Player's name can't be empty!")

                # Cancel operation
                elif new_name_input == "0":
                    print("\n⚠️ No players were added.")
                    break

                # Validate player name
                elif new_name_input in existing_players:
                    print(f"\n⚠️ Player '{new_name_input}' already exists! Please choose a different name.")

                else:
                    # Rename player to the database
                    connector.cur.execute(query_rename_player, (new_name_input, player_id))
                    connector.commit()
                    print(f"\n✅ Player '{player_name}' successfully changed name to '{new_name_input}'")
                break
            break

def delete_player():
    # Get all players
    data_players = get_all_players_data()

    if not data_players:
        print("\n⚠️ No players available. Please add players first!")
        return

    while True:
        print("\n=== Delete Player ===")
        print_players(data_players)
        print("⚠️ Type 0 to back")

        try:
            index_input = int(input("\nChoose player to delete: ").strip())
        except ValueError:
            print("\n❌ Invalid input! Please enter a valid number.\n")
            continue

        if index_input == 0:
            break
        elif not (1 <= index_input <= len(data_players)):
            print("\n❌ Invalid selection. Please choose a number from the list!\n")
        else:
            # Get actual player ID and name
            player_id, player_name = data_players[index_input - 1]

            # Delete player from database
            connector.cur.execute(query_delete_player, (player_id,))
            update_total_win(data_players)
            connector.commit()

            print(f"\n✅ Player '{player_name}' deleted successfully!")
            break
