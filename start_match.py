from singleton import connect_database as connector
from singleton import players
from singleton import matches

# remaining match data if winner_id null
remain_matches = matches.get_remain_data

players_data = players.get_all_data
players_id = list(zip(*players_data))[0]

if not remain_matches:
    print("\nNo matches available. Generate new matches first.")
else:
    for match in remain_matches:
        match_id = match[0]
        player1_id = match[1]
        player2_id = match[3]
        player1_name = match[2]
        player2_name = match[4]

        print(f"\nMatch: {player1_name} vs {player2_name}")
        print("Please enter '1' for player 1 or '2' for player 2.")
        print("Leave blank and press Enter to skip the match.\n")

        while True:
            winner_choice = input(f"Enter your choice (1 for {player1_name} / 2 for {player2_name}): ").strip()
            if winner_choice == "1":
                connector.c.execute(matches.set_winner, (player1_id, match_id))
                connector.c.execute(matches.set_total_win, (player1_id,))
                print(f"\n✅ Winner recorded: {player1_name}!")
                break

            elif winner_choice == "2":
                connector.c.execute(matches.set_winner, (player2_id, match_id))
                connector.c.execute(matches.set_total_win, (player2_id,))
                print(f"\n✅ Winner recorded: {player2_name}!")
                break

            elif winner_choice == "":
                print(f"\n⚠️ Match between {player1_name} and {player2_name} skipped.")
                break

            else:
                print("\n❌ Invalid choice! Please enter '1' or '2' to record a winner or leave blank to skip.")

connector.c.execute(matches.set_total_win, players_id)
connector.db.commit()

# finally closing the database connection
connector.db.close()

