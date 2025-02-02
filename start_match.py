from singleton import connect_database as connector
from singleton import players
from singleton import matches

# update statement for matches
matches_update = """
    UPDATE matches
    SET winner_id = %s
    WHERE id = %s
"""

# remaining match data if winner_id null
remain_matches = matches.get_remain_data

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
                winner = player1_name
                # execute the update query to modify
                connector.c.execute(matches_update, (player1_id, match_id))
                print(f"\n✅ Winner recorded: {winner}!")
                break

            elif winner_choice == "2":
                winner = player2_name
                # execute the update query to modify
                connector.c.execute(matches_update, (player2_id, match_id))
                print(f"\n✅ Winner recorded: {winner}!")
                break

            elif winner_choice == "":
                print(f"\n⚠️ Match between {player1_name} and {player2_name} skipped.")
                break

            else:
                print("\n❌ Invalid choice! Please enter '1' or '2' to record a winner or leave blank to skip.")

connector.db.commit()

# finally closing the database connection
connector.db.close()

