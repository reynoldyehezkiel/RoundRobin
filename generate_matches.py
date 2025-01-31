from singleton import connect_database as connector

# insert statement for matches
matches_insert = """
    INSERT INTO matches
        (players1_id, players1_id)
    VALUES
        (%s, %s)
"""

# we save all the row data to be inserted in a data variable
players_data = []

print("\n--- Generating New Matches ---")
# code Here
#
#
#
#

# convert list to list of tuples
players_data = zip(*[iter(players_data)]*1)

# execute the insert commands for all rows and commit to the database
# c.executemany(matches_insert, matches_data)
connector.db.commit()

# finally closing the database connection
connector.db.close()