from query.player import *
from query.match import *

def add_players():
    # Get existing players from the database
    data_players = get_all_players_data()
    existing_players = set(name for _, name in data_players) if data_players else set()

    print("\n=== Add New Players ===")
    print("Please enter player names one by one.")
    print("⚠️ Type 'done' when you are finished adding players.\n")

    new_players = []  # List to store newly added players

    while True:
        # Asking for player name with instructions
        name_input = input("Enter a player name: ").strip()

        if name_input.lower() == "done":
            if new_players:
                # Commit new players to the database
                print(new_players)
                connector.cur.executemany(query_insert_player, new_players)
                connector.commit()
                print(f"\n✅ Finished adding {len(new_players)} players.")
            else:
                print("\n⚠️ No players added.")
            break

        # Validate player name
        elif name_input == "":
            print("\n⚠️ Player name cannot be empty. Please try again.\n")
        elif name_input in existing_players:
            print(f"\n⚠️ Player '{name_input}' already exists! Please choose a different name.\n")
        else:
            # Add new player to the list
            new_players.append((None,name_input))  # Assuming player ID is auto-generated
            existing_players.add(name_input)  # Add to the set of existing players

def retrieve_leaderboard():
    data_players = get_leaderboard()

    if not data_players:
        print("\n⚠️ No players available. Please add players first!")
        return

    # Print the leaderboard header
    print("\n--------- Leaderboard ---------")
    print(f"{'Rank':<5} {'Player':<19} {'Wins':>5}")
    print("-" * 31)

    rank = 0
    prev_win = None

    for idx, (pid, name, total_win) in enumerate(data_players, start=1):
        if total_win != prev_win:
            rank = idx  # Update rank only if the number of wins is different
        prev_win = total_win
        print(f"{rank:<5} {name:<16} {total_win:>5}")

    print("-" * 31)

def rename_player():
    print("\n⚠️ This feature is under development!")

def delete_player():
    # Get all players
    data_players = get_all_players_data()

    if not data_players:
        print("\n⚠️ No players available. Please add players first!")
        return

    # Create a dictionary {player_id: player_name} for quick lookup
    player_dict = {player[0]: player[1] for player in data_players}

    while True:
        print("\n=== Delete Player ===")
        print_players(data_players)  # Print all players
        print("⚠️ Type 0 to cancel")

        try:
            id_input = int(input("\nChoose player to delete: ").strip())
        except ValueError:
            print("\n❌ Invalid input! Please enter a valid player ID.\n")
            continue  # Restart the loop if input is not an integer

        if id_input == 0:
            print("\n⚠️ No players were deleted.")
            break
        elif id_input not in player_dict:
            print("\n❌ Player is not in the list. Make sure to input the right ID!\n")
        else:
            player_name = player_dict[id_input]

            # Delete player from database
            connector.cur.execute(query_delete_player, (id_input,))
            update_total_win(data_players)
            connector.commit()

            print(f"\n✅ Player '{player_name}' deleted successfully!")
            break

