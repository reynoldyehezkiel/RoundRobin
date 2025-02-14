from query.connection import *

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

connector.cur.execute(players_create)
connector.cur.execute(matches_create)

# print the table details
connector.cur.execute("desc players")
for i in connector.cur:
	print(i)
connector.cur.execute("desc matches")
for i in connector.cur:
	print(i)

# finally closing the database connection
connector.close()
