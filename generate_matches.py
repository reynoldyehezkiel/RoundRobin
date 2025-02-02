from itertools import combinations

from singleton import connect_database as connector
from singleton import players
from singleton import matches

# insert statement for matches
matches_insert = """
    INSERT INTO matches
        (player1_id, player2_id)
    VALUES
        (%s, %s)
"""

players_data = players.get_all_data
if not players_data:
    print("\nNo players available. Please add players first.")
else:
    # Get all existing matches
    matches_data = matches.get_all_data

    # Separate existing match data to player 1 id and player 2 id
    player1_data = list(zip(*matches_data))[1]
    player2_data = list(zip(*matches_data))[2]

    # Reconstruct existing match data to "(player1_id, player2_id)"
    existing_matches = []
    for i in range(0, len(matches_data)):
        match_list = (player1_data[i], player2_data[i])
        existing_matches.append(match_list)

    # Generate new matches for players that haven't been matched yet
    if not existing_matches:
        existing_matches = set()

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
        connector.c.executemany(matches_insert, new_matches)
        connector.db.commit()
        print("\n--- Generating New Matches ---")
        print(f"{len(new_matches)} new matches generated and added to the database!")
    else:
        print("No new matches to generate (matches already exist).")

# finally closing the database connection
connector.db.close()