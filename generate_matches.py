from itertools import combinations

from query import connect_database as connector
from query import players
from query import matches

players_data = players.get_all_data
if not players_data:
    print("\nNo players available. Please add players first.")
else:
    # Get all existing matches
    matches_data = matches.get_all_data

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
        connector.c.executemany(matches.query_insert, new_matches)
        connector.db.commit()
        print("\n--- Generating New Matches ---")
        print(f"{len(new_matches)} new matches generated and added to the database!")
    else:
        print("No new matches to generate (matches already exist).")

# finally closing the database connection
connector.db.close()