from itertools import combinations

from singleton import connect_database as connector
from singleton import get_players
from singleton import get_matches

# insert statement for matches
matches_insert = """
    INSERT INTO matches
        (player1_id, player2_id)
    VALUES
        (%s, %s)
"""

print("\n--- Generating New Matches ---")
players_data = get_players.data
if not players_data:
    print("\nNo players available. Please add players first.")

# Get all existing matches
matches_data = get_matches.data

player_1 = list(zip(*matches_data))[1]
# print(player_1)

player_2 = list(zip(*matches_data))[2]
# print(player_2)

existing_matches = []
for i in range(0, len(matches_data)):
    match_list = (list(zip(*matches_data))[1][i], list(zip(*matches_data))[2][i])
    existing_matches.append(match_list)

# Generate new matches for players that haven't been matched yet
if not existing_matches:
    existing_matches = set()

new_matches = []

# Get player id
player_id = list(zip(*players_data))[0]

# existing_matches = list(zip(*existing_matches))[1]
# print(existing_matches)

# Generate new matches for players that haven't been matched yet
for match in combinations(player_id, 2):
    match = tuple(sorted(match))
    if match not in existing_matches:
        new_matches.append(match)

# print(new_matches)

# Add only the new matches
if new_matches:
    # execute the insert commands for all rows and commit to the database
    connector.c.executemany(matches_insert, new_matches)
    connector.db.commit()
    print(f"{len(new_matches)} new matches generated and added to the database!")
else:
    print("No new matches to generate (matches already exist).")

# finally closing the database connection
connector.db.close()