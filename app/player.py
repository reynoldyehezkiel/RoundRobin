from query.player import *
from query.match import *


def add_players():
    temp_players = []
    new_players = []

    data_players = get_all_players_data()
    if data_players:
        data_players = list(zip(*data_players))[1]

    print("\n=== Add New Players ===")
    print("Please enter player names one by one.")
    print("⚠️ Type 'done' when you are finished adding players.\n")

    while True:
        # Asking for player name with instructions
        name_input = input("Enter a player name: ").strip()

        if name_input in data_players:
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
    data_players = get_leaderboard()
    if not data_players:
        print("\n⚠️ No players available. Please add players first!")
    else:
        # Print the rank, player name, and number of wins in aligned format
        print("\n--------- Leaderboard ---------")
        print(f"{'Rank':<5} {'Player':<19} {'Wins':>5}")
        print("-" * 31)

        rank = 0
        prev_win = None
        for idx, (pid, name, total_win) in enumerate(data_players, start=1):
            if total_win != prev_win:
                rank = idx  # Update rank only if score is different
            prev_win = total_win
            print(f"{rank:<6}{name:<20} {str(total_win)}")
        print("-" * 31)

# def rename_player():

def delete_player():
    # Get all players name
    data_players = get_all_players_data()

    if not data_players:
        print("\n⚠️ No players available. Please add players first!")
    else:
        # Get id player
        player_id = list(zip(*data_players))[0]

        while True:

            print("\n=== Delete Player ===")

            # Print all players data
            print_players(data_players)
            print("⚠️ Type 0 to cancel")
            id_input = int(input("\nChoose player to delete: ").strip())

            if id_input == 0:
                print(f"\n⚠️ No players are deleted.")
                break
            elif id_input not in player_id:
                print(f"\n❌ Player is not in the list. Make sure to input the right ID!\n")
            else:
                # Get player name
                player_name = ""
                for i in range(0, len(data_players)):
                    if id_input == data_players[i][0]:
                        player_name = data_players[i][1]

                # update total win
                data_total_win = update_total_win(data_players)

                connector.cur.execute(query_delete_player, (id_input,))
                connector.cur.executemany(query_update_total_win, data_total_win)
                connector.commit()

                print(f"\n✅ Player '{player_name}' deleted successfully!")
                break
