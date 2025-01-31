import connect_database as connector

# cursor object c
c = connector.db.cursor()

# create statement for players
players_create = """
	CREATE TABLE players
	(
    	id INT AUTO_INCREMENT PRIMARY KEY,
    	name VARCHAR(255) NOT NULL,
    	total_win INT DEFAULT 0,
    	created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
	)
"""

# create statement for matches
matches_create = """
	CREATE TABLE matches
	(
		id INT AUTO_INCREMENT PRIMARY KEY,
		player1_id INT NOT NULL,
		player2_id INT NOT NULL,
		winner_id INT,
		FOREIGN KEY (player1_id) REFERENCES players(id) ON DELETE CASCADE,
		FOREIGN KEY (player2_id) REFERENCES players(id) ON DELETE CASCADE,
		FOREIGN KEY (winner_id) REFERENCES players(id) ON DELETE SET NULL
	)
"""

c.execute(players_create)
c.execute(matches_create)

c = connector.db.cursor()

# fetch tblemployee details in the database
c.execute("desc players")

# print the table details
for i in c:
	print(i)

c.execute("desc matches")
# print the table details
for i in c:
	print(i)

# finally closing the database connection
connector.db.close()
