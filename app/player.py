from query.player import *
from query.match import *


def add_players():
    temp_players = []
    new_players = []

    existing_players = get_all_player_data()
    if existing_players:
        existing_players = list(zip(*existing_players))[1]

    print("\n=== Add New Players ===")
    print("Please enter player names one by one.")
    print("⚠️ Type 'done' when you are finished adding players.\n")

    while True:
        # Asking for player name with instructions
        name_input = input("Enter a player name: ").strip()

        if name_input in existing_players:
            print(f"\n⚠️ Player '{name_input}' already exists! Please choose a different name.\n")
        elif name_input == "":
            print("\n⚠️ Player name cannot be empty. Please try again.\n")
        elif name_input.lower() == "done":
            if temp_players:
                # commit database
                print("\n✅ Finished adding players.")
                connector.cur.executemany(query_insert_player, new_players)
                connector.commit()
                break
            else:
                print("\n⚠️ No players added.")
                break
        else:
            # convert list to list of tuples
            temp_players.append(name_input)
            new_players = zip(*[iter(temp_players)]*1)

def retrieve_leaderboard():
    players_data = get_leaderboard()
    if not players_data:
        print("\nNo players available. Please add players first.")
    else:
        # Print the rank, player name, and number of wins in aligned format
        print("\n--------- Leaderboard ---------")
        print(f"{'Rank':<5} {'Player':<19} {'Wins':>5}")
        print("-" * 31)

        rank = 0
        prev_win = None
        for idx, (pid, name, total_win) in enumerate(players_data, start=1):
            if total_win != prev_win:
                rank = idx  # Update rank only if score is different
            prev_win = total_win
            print(f"{rank:<6}{name:<20} {str(total_win)}")
        print("-" * 31)

# def rename_player():

def delete_player():
    # Get all players name
    players_data = get_all_player_data()

    # Get id player
    player_id = list(zip(*players_data))[0]

    while True:

        print("\n=== Delete Player ===")

        # Print all players data
        print_players(players_data)
        print("⚠️ Type 0 to cancel\n")
        id_input = int(input("\nChoose player to delete: ").strip())

        if id_input == 0:
            print(f"\nDelete player is cancel. No players are deleted.")
            break
        elif id_input not in player_id:
            print(f"\n❌ Player is not in the list. Make sure to input the right ID!\n")
        else:
            # Get player name
            player_name = ""
            for i in range(0, len(players_data)):
                if id_input == players_data[i][0]:
                    player_name = players_data[i][1]

            # update total win
            data_total_win = update_total_win(players_data)

            connector.cur.execute(query_delete_player, (id_input,))
            connector.cur.executemany(set_total_win, data_total_win)
            connector.commit()

            print(f"\n✅ Player '{player_name}' deleted successfully!")
            break
